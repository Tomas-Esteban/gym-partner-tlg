"""Servicio de progresión de pesos."""

import logging
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from gym_assistant.config.settings import Settings, get_settings
from gym_assistant.infrastructure.database.models.session import TrainingSessionModel
from gym_assistant.infrastructure.database.repositories.exercise_log_repo import (
    ExerciseLogRepository,
)
from gym_assistant.infrastructure.database.repositories.progression_repo import (
    ProgressionRepository,
)
from gym_assistant.infrastructure.database.repositories.session_repo import SessionRepository
from gym_assistant.utils.dates import week_start

logger = logging.getLogger(__name__)


class ProgressionService:
    def __init__(
        self,
        session: AsyncSession,
        settings: Settings | None = None,
    ) -> None:
        self._session = session
        self._settings = settings or get_settings()
        self._exercise_log_repo = ExerciseLogRepository(session)
        self._progression_repo = ProgressionRepository(session)
        self._session_repo = SessionRepository(session)

    async def get_suggested_weight(
        self,
        user_id: int,
        exercise_key: str,
        last_weight: float | None = None,
        increment_kg: float = 0,
    ) -> float | None:
        if last_weight is None:
            last_weight = await self._exercise_log_repo.get_last_weight(user_id, exercise_key)
        if last_weight is None:
            return None

        if increment_kg <= 0:
            return last_weight

        record = await self._progression_repo.get_latest_for_exercise(user_id, exercise_key)
        if record is None:
            return last_weight

        avg_rpe = await self._get_avg_rpe_last_active_weeks(
            user_id, self._settings.progression_weeks_threshold
        )
        if (
            record.weeks_at_current_weight >= self._settings.progression_weeks_threshold
            and avg_rpe is not None
            and avg_rpe < self._settings.progression_rpe_threshold
        ):
            suggested = last_weight + increment_kg
            logger.debug(
                "Progresión aplicada: exercise=%s, %s -> %s kg",
                exercise_key,
                last_weight,
                suggested,
            )
            return suggested

        return last_weight

    async def update_after_session(
        self,
        user_id: int,
        training_session: TrainingSessionModel,
    ) -> None:
        if training_session.completed_at is None:
            return

        current_week = week_start(training_session.completed_at.date())
        week_avg_rpe = await self._session_repo.get_avg_rpe_for_week(user_id, current_week)

        for log in training_session.exercise_logs:
            if log.weight_kg is None:
                continue

            weeks_at_weight = await self._calculate_weeks_at_weight(
                user_id=user_id,
                exercise_key=log.exercise_key,
                weight_kg=log.weight_kg,
                current_week=current_week,
            )
            await self._progression_repo.upsert(
                user_id=user_id,
                exercise_key=log.exercise_key,
                week_start=current_week,
                current_weight_kg=log.weight_kg,
                avg_session_rpe=week_avg_rpe,
                weeks_at_current_weight=weeks_at_weight,
            )
            logger.info(
                "Progresión actualizada: user=%d, exercise=%s, weight=%s, weeks=%d, rpe=%s",
                user_id,
                log.exercise_key,
                log.weight_kg,
                weeks_at_weight,
                week_avg_rpe,
            )

    async def _calculate_weeks_at_weight(
        self,
        user_id: int,
        exercise_key: str,
        weight_kg: float,
        current_week: date,
    ) -> int:
        previous = await self._progression_repo.get_latest_for_exercise(user_id, exercise_key)

        if previous is None:
            return 1

        if previous.current_weight_kg != weight_kg:
            return 1

        if previous.week_start == current_week:
            return previous.weeks_at_current_weight

        if previous.week_start < current_week:
            return previous.weeks_at_current_weight + 1

        return previous.weeks_at_current_weight

    async def _get_avg_rpe_last_active_weeks(self, user_id: int, weeks: int) -> float | None:
        active_weeks = await self._session_repo.get_recent_active_weeks(user_id, weeks)
        if not active_weeks:
            return None

        rpe_values: list[float] = []
        for active_week in active_weeks[:weeks]:
            week_rpe = await self._session_repo.get_avg_rpe_for_week(user_id, active_week)
            if week_rpe is not None:
                rpe_values.append(week_rpe)

        if not rpe_values:
            return None

        return sum(rpe_values) / len(rpe_values)
