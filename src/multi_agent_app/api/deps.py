# from fastapi import Depends
from functools import lru_cache
from ..core.graph_factory import build_full_graph

@lru_cache
def _graph_singleton():
    return build_full_graph()

def get_graph():
    return _graph_singleton()
