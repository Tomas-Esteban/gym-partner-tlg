"""Teclado inline para selección de día de entrenamiento (etapa 4)."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_day_keyboard(days: list[tuple[str, str]], suggested_key: str) -> InlineKeyboardMarkup:
    """Construye teclado con los días disponibles. El sugerido lleva estrella."""
    buttons = []
    for day_key, day_name in days:
        label = f"⭐ {day_name}" if day_key == suggested_key else day_name
        buttons.append(
            [InlineKeyboardButton(text=label, callback_data=f"day:{day_key}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
