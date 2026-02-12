"""
Chatbot LangGraph avec historique de conversation
Utilise Groq LLM pour générer des réponses
"""

from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing import TypedDict, Annotated
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


# ============================================================================
# DÉFINITION DE L'ÉTAT
# ============================================================================
class ChatState(TypedDict):
    """État du chatbot contenant les messages"""
    messages: Annotated[list[BaseMessage], add_messages]


# ============================================================================
# INITIALISATION DU LLM
# ============================================================================
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

# Modèle disponible gratuitement chez Groq


# ============================================================================
# DÉFINITION DU NŒUD DE CHAT
# ============================================================================
def chat_node(state: ChatState) -> dict:
    """
    Nœud qui traite les messages et génère une réponse du LLM

    Args:
        state: L'état contenant l'historique des messages

    Returns:
        Un dictionnaire avec la réponse du LLM
    """
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


# ============================================================================
# CONSTRUCTION DU GRAPHE
# ============================================================================
graph = StateGraph(ChatState)

# Ajouter le nœud
graph.add_node("chat_node", chat_node)

# Ajouter les arêtes
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compiler le graphe
chatbot = graph.compile()



