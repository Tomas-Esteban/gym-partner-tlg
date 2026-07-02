"""Modelo de usuario."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gym_assistant.infrastructure.database.base import Base

if TYPE_CHECKING:
    from gym_assistant.infrastructure.database.models.progression import ProgressionTrackingModel
    from gym_assistant.infrastructure.database.models.session import TrainingSessionModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    settings: Mapped[list["UserSettingModel"]] = relationship(back_populates="user")
    training_sessions: Mapped[list["TrainingSessionModel"]] = relationship(
        back_populates="user"
    )
    progression_records: Mapped[list["ProgressionTrackingModel"]] = relationship(
        back_populates="user"
    )


class UserSettingModel(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    key: Mapped[str] = mapped_column(String(100))
    value: Mapped[str] = mapped_column(String(500))

    user: Mapped["UserModel"] = relationship(back_populates="settings")
