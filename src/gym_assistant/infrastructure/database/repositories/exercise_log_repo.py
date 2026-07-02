"""Repositorio de registros de ejercicios."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gym_assistant.infrastructure.database.models.exercise_log import ExerciseLogModel


class ExerciseLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_batch(
        self,
        session_id: int,
        exercises: list[dict],
    ) -> list[ExerciseLogModel]:
        logs = []
        for ex in exercises:
            log = ExerciseLogModel(
                session_id=session_id,
                exercise_key=ex["exercise_key"],
                exercise_name=ex["exercise_name"],
                order_index=ex["order_index"],
                sets_planned=ex["sets_planned"],
                reps_planned=ex["reps_planned"],
                suggested_weight_kg=ex.get("suggested_weight_kg"),
                weight_kg=ex.get("weight_kg"),
            )
            self._session.add(log)
            logs.append(log)
        await self._session.flush()
        return logs

    async def update_weights(
        self, session_id: int, weights: list[float]
    ) -> list[ExerciseLogModel]:
        result = await self._session.execute(
            select(ExerciseLogModel)
            .where(ExerciseLogModel.session_id == session_id)
            .order_by(ExerciseLogModel.order_index)
        )
        logs = list(result.scalars().all())
        for log, weight in zip(logs, weights, strict=True):
            log.weight_kg = weight
        await self._session.flush()
        return logs

    async def get_last_weight(self, user_id: int, exercise_key: str) -> float | None:
        from gym_assistant.domain.entities import SessionStatus
        from gym_assistant.infrastructure.database.models.session import TrainingSessionModel

        result = await self._session.execute(
            select(ExerciseLogModel.weight_kg)
            .join(TrainingSessionModel)
            .where(
                TrainingSessionModel.user_id == user_id,
                TrainingSessionModel.status == SessionStatus.COMPLETED,
                ExerciseLogModel.exercise_key == exercise_key,
                ExerciseLogModel.weight_kg.isnot(None),
            )
            .order_by(TrainingSessionModel.completed_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
