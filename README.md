# 🤖 CoursAgentsLanggraph

Un cours complet pour **maîtriser LangGraph** et construire des agents IA intelligents et autonomes.

Ce projet explore les concepts fondamentaux de LangGraph à travers des exemples progressifs, du débutant à l'intermédiaire.

## 🎯 Objectif

Comprendre et maîtriser les **concepts clés de LangGraph** pour construire des systèmes d'agents IA robustes:

- ✅ Architecture des agents stateful
- ✅ Cycles de réflexion et planification
- ✅ Gestion des états et transitions
- ✅ Intégration avec des outils externes
- ✅ Patterns de contrôle de flux


## 🚀 Mise en place

### Prérequis

- **Python 3.11+**
- **pip** ou **uv** (gestionnaire de paquets moderne)

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/baneseydina/CoursAgentsLanggraph.git
cd CoursAgentsLanggraph
```

2. **Créer l'environnement virtuel**
```bash
# Avec uv (recommandé)
uv venv --python 3.11
source .venv/bin/activate

# Ou avec pip
python3.11 -m venv .venv
source .venv/bin/activate
```

3. **Installer les dépendances**
```bash
uv pip install -r requirements.txt
# ou
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et ajouter vos clés API
```

## 📖 Concepts clés de LangGraph

### 1. **État (State)**
L'état représente la mémoire du graphe à chaque étape.

```python
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    input: str
    messages: list
    output: str
```

### 2. **Nœuds (Nodes)**
Les nœuds sont les étapes du graphe - des fonctions qui traitent l'état.

```python
def processeur(state: AgentState):
    # Traiter l'état
    return {"output": "résultat"}
```

### 3. **Arêtes (Edges)**
Les arêtes connectent les nœuds et définissent le flux d'exécution.

```python
graph.add_edge("noeud1", "noeud2")
graph.add_conditional_edge("decision", route_function)
```

### 4. **Cycles de Réflexion**
Les agents réfléchissent sur leurs actions et peuvent corriger leur cours.

```python
Agent → Pense → Agit → Observe → Réfléchit → ...
```

### 5. **Gestion des Outils**
Les agents peuvent utiliser des outils pour accomplir des tâches.

```python
tools = [scrape_website, create_outline, edit_document]
agent = create_agent(llm, tools)
```

## 🎓 Niveaux d'apprentissage

### 📍 Niveau Débutant
Concepts fondamentaux de LangGraph:
- Structure de base d'un graphe
- États et transitions simples
- Nœuds et arêtes basiques
- Premier agent simple

**Fichiers d'exemple:**
- `Debutant/01_basic_graph.py` - Créer un graphe simple
- `Debutant/02_simple_agent.py` - Premier agent
- `Debutant/03_state_management.py` - Gestion d'état

### 📍 Niveau Intermédiaire
Patterns avancés et architectures réelles:
- Agents avec outils intégrés
- Boucles de réflexion (ReAct pattern)
- Gestion d'erreurs et retry logic
- Multi-étapes de planification
- Agents collaboratifs

**Fichiers d'exemple:**
- `Intermediaire/01_agent_with_tools.py` - Agent avec outils
- `Intermediaire/02_react_pattern.py` - Pattern ReAct
- `Intermediaire/03_planning_agent.py` - Agent de planification
- `Intermediaire/04_multi_agent.py` - Systèmes multi-agents

## 🛠️ Outils disponibles

Le dossier `outils/` contient les implémentations des outils:

| Outil | Description |
|-------|-------------|
| `scrape_website()` | Extraire le contenu d'URLs |
| `create_outline()` | Générer des plans structurés |
| `read_document()` | Lire des documents |
| `write_document()` | Créer des documents |
| `edit_document()` | Modifier des documents |





```


## 🔑 Concepts avancés

### Conditional Edges
Créer des branches dans le flux basées sur des conditions:
```python
def route(state):
    if state["needs_research"]:
        return "search"
    return "process"

graph.add_conditional_edge("node1", route)
```

### Memory Management
Gérer la mémoire de l'agent sur plusieurs tours:
```python
state["history"].append({"role": "user", "content": message})
```

### Error Handling
Gérer les erreurs et implémenter des retry:
```python
try:
    result = tool.execute()
except Exception as e:
    state["errors"].append(str(e))
    return "retry_node"
```

## 📦 Dépendances principales

```
langgraph>=0.0.20
langchain>=0.1.0
langchain-community>=0.0.10
langchain-openai>=0.0.5
python-dotenv>=1.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## 🧪 Tester les exemples

Chaque niveau contient des exemples exécutables:

```bash
# Exécuter tous les tests
python -m pytest

# Exécuter un exemple spécifique
python Debutant/01_basic_graph.py
```

## 📝 Notes importantes

- **Variables d'environnement**: Créez un `.env` avec vos clés API
- **Python 3.11+**: Requis pour la compatibilité complète
- **Respect des sites**: Respectez les `robots.txt` lors du web scraping

## 🤝 Contribution

Les contributions sont bienvenues pour:
- Ajouter de nouveaux exemples
- Améliorer la documentation
- Corriger les bugs

```bash
git checkout -b feature/mon-feature
git commit -m "Add: nouvelle fonctionnalité"
git push origin feature/mon-feature
```

## 📚 Ressources

- [Documentation LangGraph officielle](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://docs.langchain.com/)
- [ReAct Pattern Paper](https://arxiv.org/abs/2210.03629)
- [Agents en IA](https://www.anthropic.com/research/agents)

## ⭐ Remerciements

- **LangChain & LangGraph** pour l'excellent framework
- **OpenAI & Anthropic** pour les LLMs puissants
- La communauté open-source pour l'inspiration

## 👤 Auteur

**Bane Seydina Mouhamet**
- GitHub: [@baneseydina](https://github.com/baneseydina)

## 📄 Licence

MIT License - Voir `LICENSE` pour les détails

---

**Dernière mise à jour**: Février 2025

**Conseil**: Commencez par le niveau Débutant et progressez graduellement. Chaque concept s'appuie sur les précédents!