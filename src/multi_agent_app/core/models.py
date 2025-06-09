"""Pydantic schemas shared by nodes."""
from typing_extensions import TypedDict

class State(TypedDict):
    customer_id: str | None
    messages: list
    loaded_memory: str | None
    remaining_steps: int | None
