"""
Simple State Graph - Exemple fondamental de LangGraph

Ce script démontre comment créer un graphe simple avec 3 nœuds
qui traitent une entrée utilisateur de manière séquentielle.

Conceptes couverts:
- StateGraph
- TypedDict pour les états
- Nodes et Edges
- Input/Output schemas
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ============================================================================
# ÉTAPE 1: Définir les états
# ============================================================================

class InputState(TypedDict):
    """État accepté en entrée (ce que l'utilisateur fournit)"""
    user_input: str


class OutputState(TypedDict):
    """État retourné en sortie (ce que le graphe retourne)"""
    graph_output: str


class OverAllState(TypedDict):
    """État interne partagé par tous les nœuds"""
    foo: str
    user_input: str
    graph_output: str


class PrivateState(TypedDict):
    """État spécifique utilisé par certains nœuds"""
    bar: str


# ============================================================================
# ÉTAPE 2: Créer les nœuds (fonctions qui traitent l'état)
# ============================================================================

def node_1(state: InputState) -> OverAllState:
    """
    Premier nœud: traite l'input utilisateur

    Lecture: InputState
    Écriture: OverAllState

    Transformation: "My" → "My" + "name" = "My name"
    """
    return  {"foo": state["user_input"] + "name"}


def node_2(state: OverAllState) -> PrivateState:
    """
    Deuxième nœud: enrichit les données

    Lecture: OverAllState (utilise 'foo')
    Écriture: PrivateState

    Transformation: "My name" → "My name" + "is" = "My name is"
    """
    return {"bar": state['foo'] + "is"}


def node_3(state: PrivateState) -> OutputState:
    """
    Troisième nœud: formate la réponse finale

    Lecture: PrivateState (utilise 'bar')
    Écriture: OutputState

    Transformation: "My name is" → "My name is" + "BANE Seydina"
    """
    return {"graph_output": state['bar'] + "BANE Seydina"}


# ============================================================================
# ÉTAPE 3: Construire le graphe
# ============================================================================

# Créer le builder avec l'état global, le schéma d'input et le schéma d'output
builder = StateGraph(
    OverAllState,
    input_schema=InputState,
    output_schema=OutputState
)

# ============================================================================
# ÉTAPE 4: Ajouter les nœuds
# ============================================================================

builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# ============================================================================
# ÉTAPE 5: Connecter les nœuds avec les edges
# ============================================================================

builder.add_edge(START, "node_1")  # START → node_1
builder.add_edge("node_1", "node_2")  # node_1 → node_2
builder.add_edge("node_2", "node_3")  # node_2 → node_3
builder.add_edge("node_3", END)  # node_3 → END

# ============================================================================
# ÉTAPE 6: Compiler le graphe
# ============================================================================

graph = builder.compile()






