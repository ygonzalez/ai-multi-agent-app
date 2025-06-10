# from fastapi import Depends
from functools import lru_cache
from ..core.graph_factory import build_full_graph

@lru_cache
def _build(kind: str):
    return build_full_graph(kind)

def get_graph(kind: str = "music"):
    return _build(kind)
