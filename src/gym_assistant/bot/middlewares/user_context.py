"""Middleware para contexto de usuario."""

import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import async_sessionmaker

from gym_assistant.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserContextMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self._session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        tg_user: User | None = data.get("event_from_user")
        if tg_user is None:
            return await handler(event, data)

        async with self._session_factory() as session:
            user_service = UserService(session)
            db_user = await user_service.get_or_create(
                telegram_id=tg_user.id,
                username=tg_user.username,
                display_name=tg_user.full_name,
            )
            await session.commit()
            data["db_user"] = db_user

        return await handler(event, data)
