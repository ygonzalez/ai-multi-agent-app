"""Creates & returns LangGraph objects.
"""
from langgraph.graph import StateGraph, START, END
from .models import State
from .memory import get_mem_components

def build_full_graph():
    sg = StateGraph(State)

    def echo(state: State, config):
        return {"messages": state["messages"]}

    sg.add_node("echo", echo)
    sg.add_edge(START, "echo")
    sg.add_edge("echo", END)

    short_mem, long_mem = get_mem_components()
    return sg.compile(checkpointer=short_mem,
                      store=long_mem)
