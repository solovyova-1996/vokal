"""
Keyboard for the main menu
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Выбрать категорию ✅")],
        [KeyboardButton("Загрузить ⬇")],
        [KeyboardButton("Изменить ✏")],
        [KeyboardButton("Удалить ❌")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

cancel_button = KeyboardButton("Отмена")
cancel_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
intermediate_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Добавить ещё"), KeyboardButton("Закончить")],
        [KeyboardButton("Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
yes_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Да"), KeyboardButton("Нет")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def create_keyboard_category(list_category):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for category in list_category:
        keyboard.add(KeyboardButton(category))
    keyboard.add(cancel_button)
    return keyboard


def create_all_audio(list_audio):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for data in list_audio:
        text = f'Имя: {data.get("name")}|file: {data.get("file")}|параметры: {data.get("params")}'

        button = KeyboardButton(text=text)
        keyboard.add(button)
    keyboard.add(cancel_button)
    return keyboard
