# Docker & Docker Compose

This project provides Docker configurations to containerize the FastAPI backend and Streamlit frontend.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Fill in your `OPENAI_API_KEY`, `LANGSMITH_API_KEY`, and (optionally) update `BACKEND_URL` in `.env`.

## Build & Run

```bash
docker-compose up --build
```

After startup:
- FastAPI backend: http://localhost:8000  
- Streamlit frontend: http://localhost:8501
