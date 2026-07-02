"""Repositorio de sesiones de entrenamiento."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from gym_assistant.domain.entities import SessionStatus
from gym_assistant.infrastructure.database.models.session import TrainingSessionModel


class SessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: int,
        routine_name: str,
        routine_version: str,
        day_key: str,
        warmup_type: str,
    ) -> TrainingSessionModel:
        training_session = TrainingSessionModel(
            user_id=user_id,
            routine_name=routine_name,
            routine_version=routine_version,
            day_key=day_key,
            warmup_type=warmup_type,
            status=SessionStatus.IN_PROGRESS,
        )
        self._session.add(training_session)
        await self._session.flush()
        return training_session

    async def get_by_id(self, session_id: int) -> TrainingSessionModel | None:
        result = await self._session.execute(
            select(TrainingSessionModel)
            .options(selectinload(TrainingSessionModel.exercise_logs))
            .where(TrainingSessionModel.id == session_id)
        )
        return result.scalar_one_or_none()

    async def get_in_progress(self, user_id: int) -> TrainingSessionModel | None:
        result = await self._session.execute(
            select(TrainingSessionModel).where(
                TrainingSessionModel.user_id == user_id,
                TrainingSessionModel.status == SessionStatus.IN_PROGRESS,
            )
        )
        return result.scalar_one_or_none()

    async def complete(self, session_id: int, session_rpe: int) -> None:
        training_session = await self.get_by_id(session_id)
        if training_session:
            training_session.status = SessionStatus.COMPLETED
            training_session.session_rpe = session_rpe
            training_session.completed_at = datetime.now()
            await self._session.flush()

    async def cancel(self, session_id: int) -> None:
        training_session = await self.get_by_id(session_id)
        if training_session:
            training_session.status = SessionStatus.CANCELLED
            training_session.completed_at = datetime.now()
            await self._session.flush()

    async def get_last_completed_day_key(self, user_id: int) -> str | None:
        result = await self._session.execute(
            select(TrainingSessionModel.day_key)
            .where(
                TrainingSessionModel.user_id == user_id,
                TrainingSessionModel.status == SessionStatus.COMPLETED,
            )
            .order_by(TrainingSessionModel.completed_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
