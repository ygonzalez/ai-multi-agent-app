from functools import lru_cache
from langchain_core.runnables import Runnable
from ..core.graph_factory import build_full_graph

@lru_cache(maxsize=1)
def get_graph() -> Runnable:
    """
    Get the graph, caching it to ensure it's only built once.
    """
    graph = build_full_graph()
    return graph