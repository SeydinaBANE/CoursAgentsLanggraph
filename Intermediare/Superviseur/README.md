# Guide Complet : Construction d'un Superviseur avec LangGraph

## Table des Matières
1. [Introduction](#introduction)
2. [Architecture d'un Superviseur](#architecture)
3. [Composants Clés](#composants)
4. [Implémentation Étape par Étape](#implémentation)
5. [Exemple Complet](#exemple-complet)
6. [Bonnes Pratiques](#bonnes-pratiques)
7. [Débogage](#débogage)

---

## Introduction

Un **superviseur** est un agent IA qui orchestre plusieurs travailleurs (agents spécialisés) pour accomplir une tâche complexe. Il décide quel travailleur doit agir ensuite en fonction du contexte et des résultats précédents.

### Cas d'Usage
- Orchestration d'équipes d'agents spécialisés
- Gestion de workflows multi-étapes
- Prise de décision hiérarchique
- Délégation intelligente de tâches

---

## Architecture d'un Superviseur

```
┌─────────────────────────────────────────┐
│         Utilisateur / Requête           │
└──────────────────┬──────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   Nœud Superviseur   │
        │  (Décision & Routing)│
        └────┬─────────┬────┬──┘
             │         │    │
        ┌────▼──┐ ┌────▼──┐ ┌──┴──┐
        │Agent 1│ │Agent 2│ │ ... │
        └────┬──┘ └────┬──┘ └──┬──┘
             │         │       │
             └─────┬───┴───┬───┘
                   │       │
            ┌──────▼──────▼──┐
            │  État Global   │
            │  (Historique)  │
            └────────────────┘
```

---

## Composants Clés

### 1. **État (State)**
Stocke l'historique des messages et le suivi du flux.

```python
from langgraph.graph import MessagesState

class SupervisorState(MessagesState):
    next: str  # Indique le prochain nœud à exécuter
```

### 2. **Routeur (Router)**
Structure TypedDict qui spécifie la prochaine action.

```python
from typing import TypedDict, Literal

class Router(TypedDict):
    next: Literal["agent_recherche", "agent_analyse", "FINISH"]
```

### 3. **Nœud Superviseur**
Fonction qui prend une décision basée sur l'IA.

```python
def supervisor(state: SupervisorState) -> Command:
    # Logique de décision avec LLM
    # Retourne Command avec le prochain nœud et les mises à jour d'état
```

### 4. **Nœuds Travailleurs**
Agents spécialisés qui exécutent des tâches spécifiques.

```python
def agent_recherche(state: SupervisorState) -> Command:
    # Effectuer une recherche
    return Command(update={"messages": [...]})
```

---

## Implémentation Étape par Étape

### Étape 1 : Installation des Dépendances

```bash
pip install langgraph langchain-openai python-dotenv pydantic langchain-groq
```

### Étape 2 : Définir l'État

```python
from langgraph.graph import MessagesState

class SupervisorState(MessagesState):
    next: str  # Le nœud à exécuter ensuite
```

### Étape 3 : Créer le Routeur

```python
from typing import TypedDict, Literal

class RouterOutput(TypedDict):
    next: Literal["recherche", "analyse", "synthese", "FINISH"]
```

### Étape 4 : Construire la Fonction Superviseur

```python
from langgraph.types import Command
from typing import Callable

def make_supervisor_node(llm, members: list[str]) -> Callable:
    """
    Crée un nœud superviseur qui décide quel agent activer.
    
    Args:
        llm: Modèle de langue avec structured_output
        members: Liste des noms des agents disponibles
        
    Returns:
        Fonction superviseur pour intégration dans un graphe
    """
    options = ["FINISH"] + members
    
    system_prompt = (
        "Tu es un superviseur gérant une conversation entre les travailleurs suivants : "
        f"{', '.join(members)}. "
        "En fonction de la requête utilisateur, décide quel travailleur doit agir ensuite. "
        "Chaque travailleur accomplira une tâche et répondra avec ses résultats. "
        "Quand tu as terminé, réponds avec FINISH."
    )
    
    class RouterOutput(TypedDict):
        next: Literal[tuple(options)]  # Types dynamiques possibles
    
    def supervisor(state: SupervisorState) -> Command:
        # Construire le contexte avec le prompt système
        messages = [
            {"role": "system", "content": system_prompt}
        ] + state.get("messages", [])
        
        # Appeler le LLM avec sortie structurée
        response = llm.with_structured_output(RouterOutput).invoke(messages)
        goto = response["next"]
        
        # Si terminé, aller au nœud de fin
        if goto == "FINISH":
            goto = "__end__"
        
        return Command(
            goto=goto,
            update={"next": goto}
        )
    
    return supervisor

```

### Étape 5 : Créer les Nœuds Travailleurs

```python
def create_agent_node(agent, name: str) -> Callable:
    """
    Crée un nœud travailleur qui exécute un agent.
    
    Args:
        agent: L'agent à exécuter
        name: Nom de l'agent
        
    Returns:
        Fonction nœud pour le graphe
    """
    def agent_node(state: SupervisorState) -> Command:
        result = agent.invoke(state)
        
        return Command(
            goto="supervisor",  # Revenir au superviseur
            update={
                "messages": state.get("messages", []) + [
                    {"role": "assistant", "name": name, "content": str(result)}
                ]
            }
        )
    
    return agent_node
```

### Étape 6 : Assembler le Graphe

```python
from langgraph.graph import StateGraph, START, END

def build_supervisor_graph(llm, agents: dict) -> StateGraph:
    """
    Construit le graphe complet du superviseur.
    
    Args:
        llm: Modèle de langue
        agents: Dict {nom: agent}
        
    Returns:
        Graphe compilé prêt à exécuter
    """
    workflow = StateGraph(SupervisorState)
    
    # Ajouter le nœud superviseur
    supervisor_node = make_supervisor_node(llm, list(agents.keys()))
    workflow.add_node("supervisor", supervisor_node)
    
    # Ajouter les nœuds travailleurs
    for name, agent in agents.items():
        agent_node = create_agent_node(agent, name)
        workflow.add_node(name, agent_node)
    
    # Ajouter les transitions
    for name in agents.keys():
        workflow.add_edge(name, "supervisor")  # Les agents reviennent au superviseur
    
    workflow.add_edge(START, "supervisor")  # Commencer au superviseur
    
    return workflow.compile()
```

---

## Exemple Complet

```python
import os
from typing import TypedDict, Literal
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


# ============= Configuration =============
class SupervisorState(MessagesState):
    next: str


class RouterOutput(TypedDict):
    next: Literal["recherche", "analyse", "FINISH"]


# ============= Nœud Superviseur =============
def make_supervisor_node(llm, members: list[str]):
    options = ["FINISH"] + members
    system_prompt = (
        "Tu es un superviseur gérant une conversation entre les travailleurs suivants : "
        f"{', '.join(members)}. "
        "En fonction de la requête, décide quel travailleur doit agir. "
        "Quand terminé, réponds FINISH."
    )
    
    def supervisor(state: SupervisorState) -> Command:
        messages = [{"role": "system", "content": system_prompt}] + state.get("messages", [])
        response = llm.with_structured_output(RouterOutput).invoke(messages)
        goto = response["next"]
        
        if goto == "FINISH":
            goto = "__end__"
        
        return Command(goto=goto, update={"next": goto})
    
    return supervisor


# ============= Nœud Agent Recherche =============
def agent_recherche(state: SupervisorState) -> Command:
    """Simule une recherche d'informations"""
    response = "Résultats de recherche : ...[données pertinentes]..."
    
    return Command(
        goto="supervisor",
        update={
            "messages": state.get("messages", []) + [
                {"role": "assistant", "name": "recherche", "content": response}
            ]
        }
    )


# ============= Nœud Agent Analyse =============
def agent_analyse(state: SupervisorState) -> Command:
    """Simule l'analyse des données"""
    response = "Analyse : Les données montrent que..."
    
    return Command(
        goto="supervisor",
        update={
            "messages": state.get("messages", []) + [
                {"role": "assistant", "name": "analyse", "content": response}
            ]
        }
    )


# ============= Construction du Graphe =============
def build_graph():
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    workflow = StateGraph(SupervisorState)
    
    # Ajouter les nœuds
    workflow.add_node("supervisor", make_supervisor_node(llm, ["recherche", "analyse"]))
    workflow.add_node("recherche", agent_recherche)
    workflow.add_node("analyse", agent_analyse)
    
    # Ajouter les transitions
    workflow.add_edge("recherche", "supervisor")
    workflow.add_edge("analyse", "supervisor")
    workflow.add_edge(START, "supervisor")
    
    return workflow.compile()


# ============= Exécution =============
if __name__ == "__main__":
    graph = build_graph()
    
    # Entrée initiale
    input_state = {
        "messages": [
            {"role": "user", "content": "Analyse les tendances du marché tech"}
        ]
    }
    
    # Exécuter le graphe
    for output in graph.stream(input_state, stream_mode="updates"):
        print("Mise à jour :", output)
```

---

## Bonnes Pratiques

### 1. **Prompt Clair et Structuré**
```python
system_prompt = (
    "Tu es un superviseur. "
    "Rôle : Décider quel agent utiliser. "
    f"Agents disponibles : {agents}. "
    "Instructions : Réponds TOUJOURS en JSON avec la clé 'next'."
)
```

### 2. **Gestion de l'Historique**
```python
# Garder l'historique pour le contexte
messages = state.get("messages", [])
if len(messages) > 50:  # Limiter la taille
    messages = messages[-20:]  # Garder les 20 derniers
```

### 3. **Sortie Structurée**
```python
# Toujours utiliser structured_output pour la fiabilité
response = llm.with_structured_output(RouterOutput).invoke(messages)
```

### 4. **Gestion des Erreurs**
```python
def supervisor(state: SupervisorState) -> Command:
    try:
        # Logique du superviseur
        pass
    except Exception as e:
        # Revenir au superviseur avec message d'erreur
        return Command(
            goto="supervisor",
            update={"messages": state.get("messages", []) + [
                {"role": "assistant", "content": f"Erreur : {str(e)}"}
            ]}
        )
```

### 5. **Limite de Profondeur**
```python
# Éviter les boucles infinies
if len(state.get("messages", [])) > 100:
    return Command(goto="__end__", update={})
```

---

## Débogage

### Visualiser le Graphe
```python
from IPython.display import Image, display

# Afficher la structure
display(Image(graph.get_graph().draw_mermaid_png()))
```

### Afficher les États
```python
for output in graph.stream(input_state):
    print("État :", json.dumps(output, indent=2))
```

### Logs Détaillés
```python
import logging
logging.basicConfig(level=logging.DEBUG)

for output in graph.stream(input_state, stream_mode="debug"):
    print(output)
```

---

## Ressources Utiles

- [Documentation LangGraph](https://langchain-ai.github.io/langgraph/)
- [Exemples Superviseur](https://github.com/langchain-ai/langgraph/tree/main/examples)
- [Guide Structured Output](https://python.langchain.com/docs/modules/model_io/structured_output/)

---

**Créé avec ❤️ pour la construction d'agents IA puissants**