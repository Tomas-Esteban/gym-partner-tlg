"""Servicio de progresión de pesos (etapa 8)."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ProgressionService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_suggested_weight(
        self, user_id: int, exercise_key: str, last_weight: float | None
    ) -> float | None:
        """MVP: sugerir el último peso registrado."""
        return last_weight
