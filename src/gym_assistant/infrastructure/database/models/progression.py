"""Modelo de seguimiento de progresión."""

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gym_assistant.infrastructure.database.base import Base

if TYPE_CHECKING:
    from gym_assistant.infrastructure.database.models.user import UserModel


class ProgressionTrackingModel(Base):
    __tablename__ = "progression_tracking"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    exercise_key: Mapped[str] = mapped_column(index=True)
    week_start: Mapped[date] = mapped_column(Date)
    avg_session_rpe: Mapped[float | None] = mapped_column(Float, nullable=True)
    current_weight_kg: Mapped[float] = mapped_column(Float)
    weeks_at_current_weight: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["UserModel"] = relationship(back_populates="progression_records")
