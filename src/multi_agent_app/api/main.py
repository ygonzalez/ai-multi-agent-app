from fastapi import FastAPI
from .routes import chat, chat_sse

def create_app() -> FastAPI:
    app = FastAPI(title="Multi-Agent Customer Support")
    app.include_router(chat.router)
    app.include_router(chat_sse.router)
    return app

app = create_app()
