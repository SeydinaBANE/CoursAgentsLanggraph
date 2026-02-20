from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage



# Définition de l'état du graph
class ChatState(TypedDict):
    messages: List[Dict[str, str]]


def create_graph():
    """Crée et compile le graph LangGraph."""

    # Initialisation du modèle Groq
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.7,
    )

    def chatbot_node(state: ChatState) -> ChatState:
        """Nœud principal du chatbot."""
        messages = state["messages"]

        # Conversion des messages au format LangChain
        lc_messages = [
            SystemMessage(
                content="Tu es un assistant intelligent et serviable. Réponds toujours de manière claire et précise.")
        ]

        for msg in messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))

        # Appel au LLM
        response = llm.invoke(lc_messages)

        # Ajout de la réponse à l'état
        new_messages = messages + [{"role": "assistant", "content": response.content}]
        return {"messages": new_messages}

    # Construction du graph
    builder = StateGraph(ChatState)
    builder.add_node("chatbot", chatbot_node)
    builder.set_entry_point("chatbot")
    builder.add_edge("chatbot", END)

    return builder.compile()