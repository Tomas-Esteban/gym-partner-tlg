"""Entidades y excepciones de dominio."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class SessionStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class User:
    id: int
    telegram_id: int
    username: str | None
    display_name: str | None
    created_at: datetime


@dataclass
class TrainingSession:
    id: int
    user_id: int
    routine_name: str
    routine_version: str
    day_key: str
    warmup_type: str
    session_rpe: int | None
    status: SessionStatus
    started_at: datetime
    completed_at: datetime | None


@dataclass
class ExerciseLog:
    id: int
    session_id: int
    exercise_key: str
    exercise_name: str
    order_index: int
    sets_planned: int
    reps_planned: str
    suggested_weight_kg: float | None
    weight_kg: float | None


@dataclass
class SessionSummary:
    day_key: str
    session_rpe: int
    exercises: list[tuple[str, float]]


@dataclass
class ExerciseWeightInfo:
    exercise_key: str
    exercise_name: str
    sets: int
    reps: str
    last_weight_kg: float | None
    suggested_weight_kg: float | None
