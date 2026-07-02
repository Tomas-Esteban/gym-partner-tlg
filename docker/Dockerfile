FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY alembic.ini ./
COPY alembic/ ./alembic/

RUN pip install --no-cache-dir .

RUN mkdir -p /app/data/routines/warmups

CMD ["gym-assistant"]
