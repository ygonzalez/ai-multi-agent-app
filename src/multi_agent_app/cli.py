"""Tiny REPL to poke the graph without Streamlit."""
from .core.graph_factory import build_full_graph
import uuid

def main():
    graph = build_full_graph()
    thread_id = uuid.uuid4()
    while True:
        msg = input("you> ")
        if msg.lower() in {"exit", "quit"}:
            break
        result = graph.invoke(
            {"messages": [{"role": "user", "content": msg}]},
            config={"configurable": {"thread_id": thread_id}},
        )
        print("bot>", result["messages"][-1].content)
        # print("bot>", result["messages"][-1]["content"])


if __name__ == "__main__":
    main()
