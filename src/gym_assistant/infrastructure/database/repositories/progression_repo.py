"""Repositorio de seguimiento de progresión."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gym_assistant.infrastructure.database.models.progression import ProgressionTrackingModel


class ProgressionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_latest_for_exercise(
        self, user_id: int, exercise_key: str
    ) -> ProgressionTrackingModel | None:
        result = await self._session.execute(
            select(ProgressionTrackingModel)
            .where(
                ProgressionTrackingModel.user_id == user_id,
                ProgressionTrackingModel.exercise_key == exercise_key,
            )
            .order_by(ProgressionTrackingModel.week_start.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_for_week(
        self, user_id: int, exercise_key: str, week_start: date
    ) -> ProgressionTrackingModel | None:
        result = await self._session.execute(
            select(ProgressionTrackingModel).where(
                ProgressionTrackingModel.user_id == user_id,
                ProgressionTrackingModel.exercise_key == exercise_key,
                ProgressionTrackingModel.week_start == week_start,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self,
        user_id: int,
        exercise_key: str,
        week_start: date,
        current_weight_kg: float,
        avg_session_rpe: float | None,
        weeks_at_current_weight: int,
    ) -> ProgressionTrackingModel:
        record = await self.get_for_week(user_id, exercise_key, week_start)
        if record:
            record.current_weight_kg = current_weight_kg
            record.avg_session_rpe = avg_session_rpe
            record.weeks_at_current_weight = weeks_at_current_weight
        else:
            record = ProgressionTrackingModel(
                user_id=user_id,
                exercise_key=exercise_key,
                week_start=week_start,
                current_weight_kg=current_weight_kg,
                avg_session_rpe=avg_session_rpe,
                weeks_at_current_weight=weeks_at_current_weight,
            )
            self._session.add(record)
        await self._session.flush()
        return record
