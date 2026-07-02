"""Modelo de sesión de entrenamiento."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gym_assistant.infrastructure.database.base import Base

if TYPE_CHECKING:
    from gym_assistant.infrastructure.database.models.exercise_log import ExerciseLogModel
    from gym_assistant.infrastructure.database.models.user import UserModel


class TrainingSessionModel(Base):
    __tablename__ = "training_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    routine_name: Mapped[str] = mapped_column(String(255))
    routine_version: Mapped[str] = mapped_column(String(50))
    day_key: Mapped[str] = mapped_column(String(50))
    warmup_type: Mapped[str] = mapped_column(String(50))
    session_rpe: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), index=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["UserModel"] = relationship(back_populates="training_sessions")
    exercise_logs: Mapped[list["ExerciseLogModel"]] = relationship(
        back_populates="session", order_by="ExerciseLogModel.order_index"
    )
