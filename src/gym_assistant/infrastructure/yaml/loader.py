"""Cargador de rutinas y calentamientos desde YAML."""

import logging
from pathlib import Path

import yaml

from gym_assistant.domain.exceptions import RoutineNotFoundError
from gym_assistant.infrastructure.yaml.schemas import DaySchema, RoutineSchema, WarmupSchema

logger = logging.getLogger(__name__)

ROUTINE_FILENAME = "routine.yaml"
WARMUPS_DIR = "warmups"


class RoutineLoader:
    def __init__(self, routines_path: Path) -> None:
        self._routines_path = routines_path
        self._routine: RoutineSchema | None = None
        self._warmups: dict[str, WarmupSchema] = {}

    @property
    def routine(self) -> RoutineSchema:
        if self._routine is None:
            raise RoutineNotFoundError("Rutina no cargada. Llama a load() primero.")
        return self._routine

    def load(self) -> RoutineSchema:
        routine_path = self._routines_path / ROUTINE_FILENAME
        if not routine_path.exists():
            raise RoutineNotFoundError(f"Archivo de rutina no encontrado: {routine_path}")

        with routine_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self._routine = RoutineSchema.model_validate(data)
        self._warmups.clear()
        logger.info(
            "Rutina cargada: %s v%s (%d días)",
            self._routine.name,
            self._routine.version,
            len(self._routine.days),
        )
        return self._routine

    def get_warmup(self, warmup_type: str) -> WarmupSchema:
        if warmup_type not in self._warmups:
            warmup_path = self._routines_path / WARMUPS_DIR / f"{warmup_type}.yaml"
            if not warmup_path.exists():
                raise RoutineNotFoundError(f"Calentamiento no encontrado: {warmup_type}")
            with warmup_path.open(encoding="utf-8") as f:
                data = yaml.safe_load(f)
            self._warmups[warmup_type] = WarmupSchema.model_validate(data)

        return self._warmups[warmup_type]

    def get_day(self, day_key: str) -> DaySchema:
        day = self.routine.get_day(day_key)
        if day is None:
            raise RoutineNotFoundError(f"Día no encontrado: {day_key}")
        return day
