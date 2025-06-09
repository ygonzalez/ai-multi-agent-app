from fastapi import APIRouter, Depends
from pydantic import BaseModel
import uuid
from ..deps import get_graph

router = APIRouter()

class ChatReq(BaseModel):
    message: str
    thread_id: str | None = None

class ChatResp(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResp)
async def chat(req: ChatReq, graph = Depends(get_graph)):
    tid = req.thread_id or str(uuid.uuid4())
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": req.message}]},
        config={"configurable": {"thread_id": tid}},
    )
    # FastAPI will serialise the dict to JSON automatically
    return {"response": result["messages"][-1]["content"]}

