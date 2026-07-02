"""Handlers de comandos comunes."""

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current = await state.get_state()
    if current is None:
        await message.answer("No hay ninguna operación en curso.")
        return

    await state.clear()
    logger.info("Sesión cancelada por usuario telegram_id=%d", message.from_user.id)
    await message.answer("Operación cancelada.")
