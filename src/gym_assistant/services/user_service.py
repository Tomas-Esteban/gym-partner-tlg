"""Servicio de usuarios."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from gym_assistant.infrastructure.database.models.user import UserModel
from gym_assistant.infrastructure.database.repositories.user_repo import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserRepository(session)

    async def get_or_create(
        self,
        telegram_id: int,
        username: str | None = None,
        display_name: str | None = None,
    ) -> UserModel:
        user, created = await self._repo.get_or_create(telegram_id, username, display_name)
        if created:
            logger.info("Nuevo usuario registrado: telegram_id=%d", telegram_id)
        return user
