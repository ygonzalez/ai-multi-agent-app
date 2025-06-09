# Dockerfile for FastAPI backend service
FROM python:3.13-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install poetry
RUN pip install --upgrade pip \
    && pip install poetry

WORKDIR /app

# Copy dependency definitions and project metadata for caching
COPY pyproject.toml poetry.lock README.md ./
# Copy source code for packaging
COPY src ./src

# Install dependencies (excluding development dependencies)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

# Copy the full application code
COPY . .

# Expose the application port
EXPOSE 8000

# Default command: run the FastAPI app with Uvicorn
CMD ["uvicorn", "multi_agent_app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]