FROM python:3.12-slim-bookworm as base-builder
    # python

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV="/venv"

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# prepare virtual env
RUN python -m venv $VIRTUAL_ENV

# working directory and Python path
WORKDIR /app

ENV PYTHONPATH="/app:$PYTHONPATH"

COPY pyproject.toml ./

COPY src/ ./src
COPY alembic/ ./alembic
COPY alembic.ini ./alembic.ini

RUN pip install -e .

EXPOSE 8000

FROM base-builder as dev

CMD ["echo", "CMD Backend Dev"]

FROM base-builder as prod

CMD ["echo", "CMD Backend Prod"]
