"""Utilidades para parseo de pesos."""

from gym_assistant.domain.exceptions import InvalidWeightFormatError


def parse_weights_message(text: str) -> list[float]:
    """Parsea un mensaje multilínea de pesos (uno por línea)."""
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        raise InvalidWeightFormatError("(vacío)")

    weights: list[float] = []
    for line in lines:
        normalized = line.replace(",", ".")
        try:
            weight = float(normalized)
        except ValueError as exc:
            raise InvalidWeightFormatError(line) from exc
        if weight < 0:
            raise InvalidWeightFormatError(line)
        weights.append(weight)

    return weights
