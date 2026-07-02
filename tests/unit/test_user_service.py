"""Tests del servicio de usuarios."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from gym_assistant.infrastructure.database.base import Base
from gym_assistant.infrastructure.database.models import UserModel  # noqa: F401
from gym_assistant.services.user_service import UserService


@pytest.fixture
async def db_session(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession) -> None:
    service = UserService(db_session)
    user = await service.get_or_create(
        telegram_id=123456,
        username="testuser",
        display_name="Test User",
    )
    await db_session.commit()

    assert user.id is not None
    assert user.telegram_id == 123456
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_get_existing_user(db_session: AsyncSession) -> None:
    service = UserService(db_session)
    user1 = await service.get_or_create(telegram_id=789, username="user1")
    await db_session.commit()

    user2 = await service.get_or_create(telegram_id=789, username="user1_updated")
    assert user1.id == user2.id
