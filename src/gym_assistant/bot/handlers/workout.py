"""Handler del flujo de entrenamiento."""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from gym_assistant.bot.formatters.workout import (
    format_warmup_message,
    format_weights_saved,
    format_workout_sheet,
)
from gym_assistant.bot.keyboards.day_selection import build_day_keyboard
from gym_assistant.bot.states.workout import WorkoutStates
from gym_assistant.domain.exceptions import (
    InvalidWeightCountError,
    InvalidWeightFormatError,
    RoutineNotFoundError,
)
from gym_assistant.infrastructure.database.models.user import UserModel
from gym_assistant.services.routine_service import RoutineService
from gym_assistant.services.workout_service import WorkoutService
from gym_assistant.utils.weights import parse_weights_message

logger = logging.getLogger(__name__)

router = Router(name="workout")

DAY_CALLBACK_PREFIX = "day:"
FINISHED_KEYWORDS = {"terminé", "termine", "terminé.", "termine."}


@router.message(F.text.lower() == "gym")
async def cmd_gym(
    message: Message,
    state: FSMContext,
    db_user: UserModel,
    routine_service: RoutineService,
    session_factory: async_sessionmaker,
) -> None:
    await state.clear()

    async with session_factory() as session:
        workout_service = WorkoutService(session)
        await workout_service.cancel_in_progress_session(db_user.id)
        last_day_key = await workout_service.get_last_completed_day_key(db_user.id)
        await session.commit()

    suggested_key = routine_service.get_suggested_day_key(last_day_key)
    suggested_day = routine_service.get_day(suggested_key)
    days = routine_service.get_all_day_keys()

    await message.answer(
        "¿Vas a entrenar?\n\n"
        f"Te sugiero: <b>{suggested_day.name}</b>\n"
        "Elegí el día:",
        reply_markup=build_day_keyboard(days, suggested_key),
    )
    await state.set_state(WorkoutStates.awaiting_day)
    logger.info(
        "Entrenamiento iniciado: user_id=%d, sugerido=%s",
        db_user.id,
        suggested_key,
    )


@router.callback_query(
    WorkoutStates.awaiting_day,
    F.data.startswith(DAY_CALLBACK_PREFIX),
)
async def on_day_selected(
    callback: CallbackQuery,
    state: FSMContext,
    db_user: UserModel,
    routine_service: RoutineService,
    session_factory: async_sessionmaker,
) -> None:
    if callback.data is None or callback.message is None:
        return

    day_key = callback.data.removeprefix(DAY_CALLBACK_PREFIX)

    try:
        day = routine_service.get_day(day_key)
        warmup = routine_service.get_warmup(day.warmup)
    except RoutineNotFoundError:
        await callback.answer("Día no válido. Intentá de nuevo.", show_alert=True)
        return

    async with session_factory() as session:
        workout_service = WorkoutService(session)
        training_session = await workout_service.start_session(
            user_id=db_user.id,
            routine=routine_service.routine,
            day=day,
        )
        session_id = training_session.id
        await session.commit()

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(format_warmup_message(warmup))
    await callback.message.answer(format_workout_sheet(day))

    await state.update_data(
        day_key=day_key,
        exercise_count=len(day.exercises),
        session_id=session_id,
    )
    await state.set_state(WorkoutStates.awaiting_weights)

    logger.info("Día seleccionado: day_key=%s, session_id=%d", day_key, session_id)


@router.message(WorkoutStates.awaiting_weights, F.text)
async def on_weights_received(
    message: Message,
    state: FSMContext,
    session_factory: async_sessionmaker,
) -> None:
    if message.text is None:
        return

    text = message.text.strip()
    if text.lower() in FINISHED_KEYWORDS:
        await message.answer(
            "Primero enviá los pesos (uno por línea, en orden de los ejercicios)."
        )
        return

    data = await state.get_data()
    session_id = data.get("session_id")
    exercise_count = data.get("exercise_count")

    if session_id is None or exercise_count is None:
        await message.answer("Error interno. Enviá gym para empezar de nuevo.")
        await state.clear()
        return

    try:
        weights = parse_weights_message(text)
    except InvalidWeightFormatError as exc:
        logger.warning("Formato de peso inválido: %s", exc.value)
        await message.answer(
            f'No pude leer el peso "<code>{exc.value}</code>". '
            "Enviá solo números, uno por línea."
        )
        return

    try:
        async with session_factory() as session:
            workout_service = WorkoutService(session)
            saved = await workout_service.save_weights(session_id, weights, exercise_count)
            await session.commit()
    except InvalidWeightCountError as exc:
        logger.warning(
            "Cantidad de pesos incorrecta: recibidos=%d, esperados=%d",
            exc.received,
            exc.expected,
        )
        await message.answer(
            f"Recibí <b>{exc.received}</b> pesos pero la rutina tiene "
            f"<b>{exc.expected}</b> ejercicios.\n"
            "Corregí y enviá de nuevo todos los pesos en un solo mensaje."
        )
        return

    await message.answer(format_weights_saved(saved))
    await state.set_state(WorkoutStates.awaiting_rpe)
    logger.info("Pesos guardados: session_id=%d, count=%d", session_id, len(saved))
