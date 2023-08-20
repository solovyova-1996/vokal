from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAudio(StatesGroup):
    name = State()
    start = State()

    param_1 = State()
    param_2 = State()
    end = State()
