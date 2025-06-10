from .music_subagent import create_music_subagent
from .invoice_subagent import create_invoice_subagent
from .supervisor import create_supervisor_agent


def build_full_graph(kind: str = "supervisor"):
    """
    kind: "music" | "invoice" | "supervisor"
    """
    if kind == "invoice":
        return create_invoice_subagent()
    if kind == "supervisor":
        return create_supervisor_agent()
    return create_music_subagent()
