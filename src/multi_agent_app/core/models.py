from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.managed.is_last_step import RemainingSteps

class State(TypedDict):
    """
    State schema for the multi-agent customer support workflow.
    Each node in the graph reads and writes to this State.
    """
    customer_id: str

    # Conversation history with auto message aggregation
    messages: Annotated[list[AnyMessage], add_messages]

    # Any user preferences loaded from long-term memory
    loaded_memory: str

    # Prevent infinite loops
    remaining_steps: RemainingSteps
