# syntax=docker/dockerfile:1.4
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONPATH="/app/src"

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./

# Install dependencies with pip, using cache mount for speed
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -e .

RUN python -m spacy download en_core_web_md

COPY src/ ./src
COPY alembic/ ./alembic
COPY alembic.ini .

EXPOSE 8000
