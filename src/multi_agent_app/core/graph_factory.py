from .supervisor import create_supervisor_graph

def build_full_graph():
    """
    Builds the complete multi-agent graph by calling the supervisor creation function.
    """
    return create_supervisor_graph()