from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from ..deps import get_graph
# from langgraph.streaming import StreamEventIterator
from typing import AsyncIterator

router = APIRouter()

@router.get("/chat/stream")
async def chat_stream(message: str, thread_id: str | None = None,
                      graph = Depends(get_graph)):
    config = {"configurable": {"thread_id": thread_id}}
    stream: AsyncIterator = graph.astream_events(
        {"messages": [{"role": "user", "content": message}]},
        version="v1",  # yields .events
        config=config,
    )

    async def event_generator():
        async for ev in stream:
            if ev.data and ev.type == "message":
                yield f"data:{ev.data.content}\n\n"

    return StreamingResponse(event_generator(),
                             media_type="text/event-stream")
