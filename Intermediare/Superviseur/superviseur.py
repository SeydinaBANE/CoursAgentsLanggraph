import os
from dotenv import load_dotenv
from typing import TypedDict, Literal
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.types import Command
from langchain_groq import ChatGroq
from pydantic import BaseModel
load_dotenv()


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
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

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