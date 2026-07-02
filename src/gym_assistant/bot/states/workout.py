"""Estados FSM del flujo de entrenamiento."""

from aiogram.fsm.state import State, StatesGroup


class WorkoutStates(StatesGroup):
    awaiting_day = State()
    showing_workout = State()
    awaiting_weights = State()
    awaiting_rpe = State()
