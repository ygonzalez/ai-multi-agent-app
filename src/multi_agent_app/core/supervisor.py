from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI

from .music_subagent import create_music_subagent
from .invoice_subagent import create_invoice_subagent

def create_supervisor_graph():
    """
    Creates and compiles the supervisor graph using the prebuilt create_supervisor.

    This function instantiates the worker agents and then uses the prebuilt
    to create a supervisor that can delegate tasks to them.
    """
    # Create the specialized worker agents
    music_agent = create_music_subagent()
    invoice_agent = create_invoice_subagent()
    members = [music_agent, invoice_agent]

    # The supervisor prompt instructs the LLM on how to delegate tasks AND present the final answer
    supervisor_prompt = """You are a supervisor managing a team of two specialized agents:
- a music_catalog_subagent: This agent handles all inquiries about our music catalog, including artists, albums, and songs.
- an invoice_information_subagent: This agent handles all inquiries about customer invoices and billing.

Your primary job is to delegate tasks to the appropriate agent based on the user's request.
Do not perform the tasks yourself; use the agents to do the work.

After an agent has completed its task and returned the result, your final job is to present this information back to the user.
If the agent has provided a list, a number, or any other piece of data, present that directly to the user as the answer.
"""
    llm = ChatOpenAI(model="gpt-4o-mini")

    supervisor_graph = create_supervisor(
        model=llm,
        agents=members,
        prompt=supervisor_prompt,
        # output_mode="last_message",
    ).compile()

    return supervisor_graph