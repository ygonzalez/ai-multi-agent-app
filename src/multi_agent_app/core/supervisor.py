from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from .music_subagent import create_music_subagent
from .invoice_subagent import create_invoice_subagent
from .models import State
from .memory import get_mem_components

# ── Supervisor prompt — tells the router how to pick a sub-agent ────────────
SUPERVISOR_PROMPT = """
You are a senior customer-support planner for a digital music store.

You have two specialist teammates:
1. music_catalog_subagent
   • Answers questions about albums, tracks, artists, genres
2. invoice_information_subagent
   • Answers billing or invoice questions

FLOW RULES
• Read the latest user message and the conversation history.
• Decide which sub-agent is best suited for the next step.
• When one sub-agent finishes, you may route to the other—or end—until the
  original user request is fully addressed.
"""

def create_supervisor_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    music_agent   = create_music_subagent()
    invoice_agent = create_invoice_subagent()

    short_mem, long_mem = get_mem_components()

    workflow = create_supervisor(
        agents=[invoice_agent, music_agent],
        output_mode="last_message",
        model=llm,
        prompt=SUPERVISOR_PROMPT,
        state_schema=State,  # keep this
    )

    supervisor_graph = workflow.compile(
        name="supervisor_agent",
        checkpointer=short_mem,
        store=long_mem,
    )
    return supervisor_graph
