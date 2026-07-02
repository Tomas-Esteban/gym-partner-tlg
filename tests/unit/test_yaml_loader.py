"""Tests del cargador YAML."""

from pathlib import Path

import pytest

from gym_assistant.infrastructure.yaml.loader import RoutineLoader


@pytest.fixture
def routines_path() -> Path:
    return Path("data/routines")


def test_load_routine(routines_path: Path) -> None:
    loader = RoutineLoader(routines_path)
    routine = loader.load()

    assert routine.name == "Rutina 4 días"
    assert routine.version == "2026-Q1"
    assert len(routine.days) == 4


def test_get_day(routines_path: Path) -> None:
    loader = RoutineLoader(routines_path)
    loader.load()

    day = loader.get_day("day_1")
    assert day.name == "Día 1 — Pecho y Tríceps"
    assert len(day.exercises) == 5


def test_get_warmup(routines_path: Path) -> None:
    loader = RoutineLoader(routines_path)
    loader.load()

    warmup = loader.get_warmup("upper")
    assert warmup.name == "Calentamiento Upper"
    assert len(warmup.steps) >= 1


def test_next_day_key(routines_path: Path) -> None:
    loader = RoutineLoader(routines_path)
    routine = loader.load()

    assert routine.get_next_day_key(None) == "day_1"
    assert routine.get_next_day_key("day_1") == "day_2"
    assert routine.get_next_day_key("day_4") == "day_1"
