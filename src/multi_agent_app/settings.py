"""Centralised env/config handling."""
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    langsmith_api_key: str | None = Field(None, env="LANGSMITH_API_KEY")
    debug: bool = False

settings = Settings()
