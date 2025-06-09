from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

def get_mem_components():
    """Returns (short_term, long_term) memory instances."""
    return MemorySaver(), InMemoryStore()
