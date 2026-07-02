"""Utilidades de fechas para progresión."""

from datetime import date, timedelta


def week_start(value: date) -> date:
    """Retorna el lunes de la semana de la fecha dada."""
    return value - timedelta(days=value.weekday())
