"""Handlers de comandos comunes."""

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from gym_assistant.infrastructure.database.models.user import UserModel
from gym_assistant.services.workout_service import WorkoutService

logger = logging.getLogger(__name__)

router = Router(name="common")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Comandos disponibles:\n\n"
        "/start — Iniciar el bot\n"
        "/help — Mostrar esta ayuda\n"
        "/cancelar — Cancelar operación en curso\n\n"
        "Para entrenar, enviá: gym"
    )


@router.message(Command("cancelar"))
async def cmd_cancel(
    message: Message,
    state: FSMContext,
    db_user: UserModel,
    session_factory: async_sessionmaker,
) -> None:
    current = await state.get_state()
    if current is None:
        await message.answer("No hay ninguna operación en curso.")
        return

    data = await state.get_data()
    session_id = data.get("session_id")
    if session_id is not None:
        async with session_factory() as session:
            workout_service = WorkoutService(session)
            await workout_service.cancel_session(session_id)
            await session.commit()

    await state.clear()
    logger.info("Sesión cancelada por usuario telegram_id=%d", message.from_user.id)
    await message.answer("Operación cancelada.")
