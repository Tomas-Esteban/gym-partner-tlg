"""Handler de /start."""

import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from gym_assistant.infrastructure.database.models.user import UserModel

logger = logging.getLogger(__name__)

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, db_user: UserModel) -> None:
    name = db_user.display_name or message.from_user.full_name
    await message.answer(
        f"Hola {name}! Soy tu Gym Assistant.\n\n"
        "Envíame *gym* cuando estés listo para entrenar.\n"
        "Usa /help para ver todos los comandos.",
        parse_mode="Markdown",
    )
