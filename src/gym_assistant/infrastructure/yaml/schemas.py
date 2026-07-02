"""Schemas Pydantic para rutinas YAML."""

from pydantic import BaseModel, Field


class ProgressionConfig(BaseModel):
    increment_kg: float = Field(default=2.5, ge=0)


class ExerciseSchema(BaseModel):
    key: str
    name: str
    sets: int = Field(gt=0)
    reps: str
    progression: ProgressionConfig = Field(default_factory=ProgressionConfig)


class DaySchema(BaseModel):
    key: str
    name: str
    warmup: str
    exercises: list[ExerciseSchema] = Field(min_length=1)


class RoutineSchema(BaseModel):
    name: str
    version: str
    cycle_days: int = Field(gt=0)
    days: list[DaySchema] = Field(min_length=1)

    def get_day(self, day_key: str) -> DaySchema | None:
        return next((d for d in self.days if d.key == day_key), None)

    def get_next_day_key(self, last_completed_day_key: str | None) -> str:
        if not last_completed_day_key:
            return self.days[0].key
        keys = [d.key for d in self.days]
        try:
            idx = keys.index(last_completed_day_key)
            return keys[(idx + 1) % len(keys)]
        except ValueError:
            return self.days[0].key


class WarmupSchema(BaseModel):
    name: str
    steps: list[str] = Field(min_length=1)
