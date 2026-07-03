FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY alembic.ini ./
COPY alembic/ ./alembic/
COPY data/routines/ /app/default-routines/
COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && pip install --no-cache-dir . \
    && mkdir -p /app/data/routines/warmups

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gym-assistant"]
