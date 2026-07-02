"""Modelo de registro de ejercicio."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gym_assistant.infrastructure.database.base import Base

if TYPE_CHECKING:
    from gym_assistant.infrastructure.database.models.session import TrainingSessionModel


class ExerciseLogModel(Base):
    __tablename__ = "exercise_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("training_sessions.id"), index=True)
    exercise_key: Mapped[str] = mapped_column(String(100), index=True)
    exercise_name: Mapped[str] = mapped_column(String(255))
    order_index: Mapped[int] = mapped_column(Integer)
    sets_planned: Mapped[int] = mapped_column(Integer)
    reps_planned: Mapped[str] = mapped_column(String(50))
    suggested_weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)

    session: Mapped["TrainingSessionModel"] = relationship(back_populates="exercise_logs")
