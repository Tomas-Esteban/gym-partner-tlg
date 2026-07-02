"""Entry point de la aplicación."""

import asyncio
import logging

from alembic import command
from alembic.config import Config

from gym_assistant.config import Settings, get_settings
from gym_assistant.utils.logging import setup_logging

logger = logging.getLogger(__name__)


def run_migrations() -> None:
    """Aplica migraciones pendientes de Alembic."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Database migrations applied")


async def run(settings: Settings) -> None:
    """Inicializa y ejecuta el bot."""
    logger.info("Bot starting...")

    from gym_assistant.bot.dispatcher import create_bot, create_dispatcher

    bot = create_bot(settings)
    dp = await create_dispatcher(settings)

    logger.info("Bot ready, polling started")
    await dp.start_polling(bot)


def main() -> None:
    """Punto de entrada síncrono."""
    settings = get_settings()
    setup_logging(settings.log_level)
    run_migrations()
    asyncio.run(run(settings))


if __name__ == "__main__":
    main()
