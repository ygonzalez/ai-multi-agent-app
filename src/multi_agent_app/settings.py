"""Centralised env/config handling."""
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    langsmith_api_key: str | None = Field(None, env="LANGSMITH_API_KEY")
    backend_url: str = Field("http://localhost:8000", env="BACKEND_URL")
    debug: bool = False

settings = Settings()
