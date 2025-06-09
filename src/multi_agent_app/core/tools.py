"""@tool-decorated SQL helpers.  Logic comes later."""
from langchain_core.tools import tool
from langchain_community.utilities.sql_database import SQLDatabase
from .db import init_memory_engine

_engine = init_memory_engine()
db = SQLDatabase(_engine)


@tool
def placeholder_tool():
    """Example stub so graph compiles."""
    return "ok"
