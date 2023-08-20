from aiogram.dispatcher.filters.state import StatesGroup, State


class ChoiceAudio(StatesGroup):
    start = State()
    end = State()
