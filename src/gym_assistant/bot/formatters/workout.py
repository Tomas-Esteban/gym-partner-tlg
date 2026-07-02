"""Formateo de mensajes de entrenamiento para Telegram."""

from gym_assistant.domain.entities import ExerciseWeightInfo
from gym_assistant.infrastructure.yaml.schemas import DaySchema, WarmupSchema

WEIGHT_PLACEHOLDER = "—"


def _format_weight(kg: float | None) -> str:
    if kg is None:
        return WEIGHT_PLACEHOLDER
    return f"{kg:g} kg"


def format_warmup_message(warmup: WarmupSchema) -> str:
    lines = [f"🔥 <b>{warmup.name}</b>\n"]
    for index, step in enumerate(warmup.steps, start=1):
        lines.append(f"{index}. {step}")
    return "\n".join(lines)


def format_workout_sheet(
    day: DaySchema,
    weight_infos: list[ExerciseWeightInfo] | None = None,
) -> str:
    info_by_key = (
        {info.exercise_key: info for info in weight_infos} if weight_infos else {}
    )

    lines = [f"📋 <b>{day.name}</b>\n"]
    for index, exercise in enumerate(day.exercises, start=1):
        info = info_by_key.get(exercise.key)
        last_weight = _format_weight(info.last_weight_kg if info else None)
        suggested_weight = _format_weight(info.suggested_weight_kg if info else None)

        lines.append(f"{index}. {exercise.name} — {exercise.sets}×{exercise.reps}")
        lines.append(f"   Último: {last_weight} | Sugerido: {suggested_weight}")
    lines.append(
        "\nCuando termines, enviá los pesos (uno por línea, en orden)."
    )
    return "\n".join(lines)


def format_weights_saved(exercise_weights: list[tuple[str, float]]) -> str:
    lines = ["✅ <b>Pesos registrados</b>\n"]
    for index, (name, weight) in enumerate(exercise_weights, start=1):
        weight_text = f"{weight:g} kg"
        lines.append(f"{index}. {name} — {weight_text}")
    return "\n".join(lines)


def format_rpe_prompt() -> str:
    return "¿Esfuerzo general de la sesión? (1–10)"


def format_session_completed(
    day_name: str,
    rpe: int,
    exercises: list[tuple[str, float]],
) -> str:
    lines = [f"🏁 <b>Sesión completada</b> — {day_name}\n", f"Esfuerzo (RPE): <b>{rpe}</b>\n"]
    for index, (name, weight) in enumerate(exercises, start=1):
        lines.append(f"{index}. {name} — {weight:g} kg")
    lines.append("\n¡Buen trabajo! Enviá <b>gym</b> cuando vuelvas a entrenar.")
    return "\n".join(lines)
