from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from .models import State
from .tools import INVOICE_TOOLS
from .memory import get_mem_components
from multi_agent_app.settings import settings


# ---------- Prompt ----------------------------------------------------------
INVOICE_PROMPT = """
You are a sub-agent specialised in invoice and billing queries.

TOOLS:
- get_invoices_by_customer_sorted_by_date: show all invoices for a customer.
- get_invoices_sorted_by_unit_price:   same invoices, ordered by highest cost.
- get_employee_by_invoice_and_customer: find the employee linked to an invoice.

If you cannot find an invoice, politely say so and ask if the customer wants to
search something else.  Ignore music-catalog questions.
"""

def create_invoice_subagent() -> "StateGraph":
    """
    Returns a compiled LangGraph ReAct agent for invoice queries.
    """
    short_mem, long_mem = get_mem_components()
    llm = ChatOpenAI(model="gpt-4o-mini",
                     api_key=settings.openai_api_key,
                     temperature=0)

    graph = create_react_agent(
        model=llm,
        tools=INVOICE_TOOLS,
        prompt=INVOICE_PROMPT,
        name="invoice_information_subagent",
        state_schema=State,
        checkpointer=short_mem,
        store=long_mem,
    )
    return graph
