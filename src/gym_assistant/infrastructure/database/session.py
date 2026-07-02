"""Engine y session factory."""

from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

_engine = None
_session_factory = None


def _ensure_sqlite_dir(database_url: str) -> None:
    """Crea el directorio de SQLite si no existe."""
    if database_url.startswith("sqlite"):
        db_path = database_url.split("///")[-1]
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)


def _to_async_url(database_url: str) -> str:
    """Convierte URL síncrona de SQLite a async."""
    if database_url.startswith("sqlite:///"):
        return database_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    return database_url


def init_engine(database_url: str) -> None:
    """Inicializa el engine y session factory."""
    global _engine, _session_factory

    _ensure_sqlite_dir(database_url)
    async_url = _to_async_url(database_url)

    _engine = create_async_engine(async_url, echo=False)
    _session_factory = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)


def get_engine():
    if _engine is None:
        raise RuntimeError("Database engine not initialized. Call init_engine first.")
    return _engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Generador de sesiones async para inyección."""
    if _session_factory is None:
        raise RuntimeError("Database engine not initialized. Call init_engine first.")
    async with _session_factory() as session:
        yield session
