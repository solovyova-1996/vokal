from aiogram.dispatcher.filters.state import StatesGroup, State


class UpdateAudio(StatesGroup):
    start = State()
    param_1 = State()
    param_2 = State()
    end = State()
