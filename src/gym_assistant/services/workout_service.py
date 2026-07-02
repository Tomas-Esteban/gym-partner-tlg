"""Servicio de entrenamientos."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from gym_assistant.domain.exceptions import InvalidWeightCountError, SessionNotFoundError
from gym_assistant.infrastructure.database.models.session import TrainingSessionModel
from gym_assistant.infrastructure.database.repositories.exercise_log_repo import (
    ExerciseLogRepository,
)
from gym_assistant.infrastructure.database.repositories.session_repo import SessionRepository
from gym_assistant.infrastructure.yaml.schemas import DaySchema, RoutineSchema

logger = logging.getLogger(__name__)


class WorkoutService:
    def __init__(self, session: AsyncSession) -> None:
        self._session_repo = SessionRepository(session)
        self._exercise_log_repo = ExerciseLogRepository(session)

    async def get_last_completed_day_key(self, user_id: int) -> str | None:
        return await self._session_repo.get_last_completed_day_key(user_id)

    async def cancel_in_progress_session(self, user_id: int) -> None:
        existing = await self._session_repo.get_in_progress(user_id)
        if existing:
            await self._session_repo.cancel(existing.id)
            logger.info("Sesión en progreso cancelada: session_id=%d", existing.id)

    async def cancel_session(self, session_id: int) -> None:
        await self._session_repo.cancel(session_id)
        logger.info("Sesión cancelada: session_id=%d", session_id)

    async def start_session(
        self,
        user_id: int,
        routine: RoutineSchema,
        day: DaySchema,
    ) -> TrainingSessionModel:
        await self.cancel_in_progress_session(user_id)

        training_session = await self._session_repo.create(
            user_id=user_id,
            routine_name=routine.name,
            routine_version=routine.version,
            day_key=day.key,
            warmup_type=day.warmup,
        )

        exercises = [
            {
                "exercise_key": exercise.key,
                "exercise_name": exercise.name,
                "order_index": index,
                "sets_planned": exercise.sets,
                "reps_planned": str(exercise.reps),
                "suggested_weight_kg": None,
            }
            for index, exercise in enumerate(day.exercises)
        ]
        await self._exercise_log_repo.create_batch(training_session.id, exercises)
        logger.info(
            "Sesión iniciada: session_id=%d, day_key=%s, ejercicios=%d",
            training_session.id,
            day.key,
            len(exercises),
        )
        return training_session

    async def save_weights(
        self,
        session_id: int,
        weights: list[float],
        expected_count: int,
    ) -> list[tuple[str, float]]:
        if len(weights) != expected_count:
            raise InvalidWeightCountError(len(weights), expected_count)

        training_session = await self._session_repo.get_by_id(session_id)
        if training_session is None:
            raise SessionNotFoundError(f"Sesión {session_id} no encontrada")

        logs = await self._exercise_log_repo.update_weights(session_id, weights)
        return [(log.exercise_name, log.weight_kg) for log in logs if log.weight_kg is not None]
