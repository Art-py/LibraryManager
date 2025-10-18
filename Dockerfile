FROM python:3.12-slim AS core

ENV POETRY_VERSION=2.2.1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock* ./

RUN poetry install --only main --no-root --no-interaction --no-ansi

FROM python:3.12-slim AS runtime

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=core /root/.cache/pypoetry /root/.cache/pypoetry
COPY --from=core /root/.local /root/.local

COPY pyproject.toml poetry.lock* ./

COPY ./src ./src
COPY ./alembic ./alembic
COPY alembic.ini .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh