from typing import NamedTuple

from aiogram.dispatcher.filters.state import StatesGroup, State

class Start(StatesGroup):
    free = State()

class CheckIn(StatesGroup):
    name = State()
    ip = State()
    disturb = State()
    canceled = State()
