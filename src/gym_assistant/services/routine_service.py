"""Servicio de rutinas."""

import logging

from gym_assistant.infrastructure.yaml.loader import RoutineLoader
from gym_assistant.infrastructure.yaml.schemas import DaySchema, RoutineSchema, WarmupSchema

logger = logging.getLogger(__name__)


class RoutineService:
    def __init__(self, loader: RoutineLoader) -> None:
        self._loader = loader

    @property
    def routine(self) -> RoutineSchema:
        return self._loader.routine

    def get_day(self, day_key: str) -> DaySchema:
        return self._loader.get_day(day_key)

    def get_warmup(self, warmup_type: str) -> WarmupSchema:
        return self._loader.get_warmup(warmup_type)

    def get_suggested_day_key(self, last_completed_day_key: str | None) -> str:
        return self._loader.routine.get_next_day_key(last_completed_day_key)

    def get_all_day_keys(self) -> list[tuple[str, str]]:
        return [(d.key, d.name) for d in self._loader.routine.days]
