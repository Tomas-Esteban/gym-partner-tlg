"""Servicio de entrenamientos."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from gym_assistant.infrastructure.database.repositories.exercise_log_repo import (
    ExerciseLogRepository,
)
from gym_assistant.infrastructure.database.repositories.session_repo import SessionRepository

logger = logging.getLogger(__name__)


class WorkoutService:
    def __init__(self, session: AsyncSession) -> None:
        self._session_repo = SessionRepository(session)
        self._exercise_log_repo = ExerciseLogRepository(session)

    async def get_last_completed_day_key(self, user_id: int) -> str | None:
        return await self._session_repo.get_last_completed_day_key(user_id)
