"""Configuración del dispatcher y bot."""

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import async_sessionmaker

from gym_assistant.bot.handlers import common, start, workout
from gym_assistant.bot.middlewares.user_context import UserContextMiddleware
from gym_assistant.config.settings import Settings
from gym_assistant.infrastructure.database.session import init_engine
from gym_assistant.infrastructure.yaml.loader import RoutineLoader
from gym_assistant.services.routine_service import RoutineService

logger = logging.getLogger(__name__)


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


async def create_dispatcher(settings: Settings) -> Dispatcher:
    init_engine(settings.database_url)

    loader = RoutineLoader(settings.routines_path)
    loader.load()
    routine_service = RoutineService(loader)

    from gym_assistant.infrastructure.database.session import get_engine

    engine = get_engine()
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    dp = Dispatcher(storage=MemoryStorage())

    dp["routine_service"] = routine_service
    dp["session_factory"] = session_factory
    dp["settings"] = settings

    dp.message.middleware(UserContextMiddleware(session_factory))

    dp.include_router(start.router)
    dp.include_router(common.router)
    dp.include_router(workout.router)

    logger.info("Dispatcher configurado con %d routers", 3)
    return dp
