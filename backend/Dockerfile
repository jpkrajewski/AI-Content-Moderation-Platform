# syntax=docker/dockerfile:1.4
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONPATH="/app/src"

RUN apt-get update && apt-get install -y curl build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./

# Install dependencies with pip, using cache mount for speed
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -e .

COPY src/ ./src
COPY alembic/ ./alembic
COPY alembic.ini .

EXPOSE 8000
