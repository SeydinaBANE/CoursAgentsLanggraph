from langgraph.graph import StateGraph,MessagesState, START, END

def hello_world(state:MessagesState):
    return {"messages":[{"role":"ai","content":"Hello world"}]}

graph = StateGraph(MessagesState)

graph.add_node("hello_world",hello_world)

graph.add_edge(START,"hello_world")
graph.add_edge("hello_world",END)

agent= graph.compile()

resp= agent.invoke({"messages":[{"role":"user","content":'Bonjour'}]})
print(resp["messages"][-1].content)