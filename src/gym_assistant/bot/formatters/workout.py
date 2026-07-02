"""Formateo de mensajes de entrenamiento para Telegram."""

from gym_assistant.infrastructure.yaml.schemas import DaySchema, WarmupSchema

WEIGHT_PLACEHOLDER = "—"


def format_warmup_message(warmup: WarmupSchema) -> str:
    lines = [f"🔥 <b>{warmup.name}</b>\n"]
    for index, step in enumerate(warmup.steps, start=1):
        lines.append(f"{index}. {step}")
    return "\n".join(lines)


def format_workout_sheet(day: DaySchema) -> str:
    lines = [f"📋 <b>{day.name}</b>\n"]
    for index, exercise in enumerate(day.exercises, start=1):
        lines.append(f"{index}. {exercise.name} — {exercise.sets}×{exercise.reps}")
        lines.append(
            f"   Último: {WEIGHT_PLACEHOLDER} | Sugerido: {WEIGHT_PLACEHOLDER}"
        )
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
