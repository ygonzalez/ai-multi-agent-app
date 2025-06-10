from fastapi import APIRouter, Depends
from pydantic import BaseModel
import uuid
from typing import Annotated
from langchain_core.runnables import Runnable
from ..deps import get_graph

router = APIRouter()


class ChatReq(BaseModel):
    message: str
    thread_id: str | None = None


class ChatResp(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResp)
async def chat(
    req: ChatReq,
    graph: Annotated[Runnable, Depends(get_graph)],
):
    tid = req.thread_id or str(uuid.uuid4())

    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": req.message}]},
        config={"configurable": {"thread_id": tid}},
    )
    return {"response": result["messages"][-1].content}