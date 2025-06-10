from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from .models import State
from .tools import MUSIC_TOOLS
from .memory import get_mem_components

from langchain_openai import ChatOpenAI

def generate_music_assistant_prompt(memory: str = "None") -> str:
    """
    Format the system prompt for the music sub-agent.
    Incorporates any loaded user preferences (memory).
    """
    return f"""
    You are a music catalog assistant. 
    You have tools for querying albums, tracks, and genres in the Chinook DB.
    Prior saved user preferences: {memory}

    CORE RESPONSIBILITIES:
    1. Provide accurate info on songs, albums, or artists.
    2. If the user query needs a DB lookup, call the appropriate tool.
    3. Otherwise, respond directly.
    """

def music_assistant(state: State, config: RunnableConfig):
    """
    The main reasoning node: decides whether to call a tool or give a final answer.
    """
    # If user memory is loaded, include it
    memory = state.get("loaded_memory", "None")

    # Build the system message
    system_content = generate_music_assistant_prompt(memory)
    system_msg = SystemMessage(system_content)

    # Bind the tools to an LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools(MUSIC_TOOLS)

    # Combine system message + conversation so far
    msgs_for_llm = [system_msg] + state["messages"]

    # The LLM returns either final text or a "tool_calls" block
    response = llm_with_tools.invoke(msgs_for_llm)

    # Add it to the messages
    return {"messages": [response]}

def should_continue(state: State, config: RunnableConfig):
    """
    Check if the last message includes a tool call.
    If so, route to the tool node; else end.
    """
    last_message = state["messages"][-1]
    if not getattr(last_message, "tool_calls", []):
        return "end"
    return "continue"

def create_music_subagent():
    sg = StateGraph(State)

    sg.add_node("music_assistant", music_assistant)
    tool_node = ToolNode(MUSIC_TOOLS)
    sg.add_node("music_tool_node", tool_node)

    sg.add_edge(START, "music_assistant")
    sg.add_conditional_edges(
        "music_assistant",
        should_continue,
        {
            "continue": "music_tool_node",
            "end": END,
        },
    )
    sg.add_edge("music_tool_node", "music_assistant")

    short_mem, long_mem = get_mem_components()

    return sg.compile(name="music_information_subagent", checkpointer=short_mem,
        store=long_mem
    )
