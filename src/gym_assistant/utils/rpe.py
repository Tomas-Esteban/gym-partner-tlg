"""Utilidades para parseo de RPE."""

from gym_assistant.domain.exceptions import InvalidRPEError

MIN_RPE = 1
MAX_RPE = 10


def parse_rpe(text: str) -> int:
    """Parsea el RPE de sesión (entero entre 1 y 10)."""
    normalized = text.strip().replace(",", ".")
    try:
        rpe = int(float(normalized))
    except ValueError as exc:
        raise InvalidRPEError(text.strip()) from exc

    if not MIN_RPE <= rpe <= MAX_RPE:
        raise InvalidRPEError(text.strip())

    return rpe
