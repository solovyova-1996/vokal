import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot import keyboards
from bot.keyboards.buttons import create_keyboard_category
from bot.loader import dp, db, bot
from bot.logger import logger
from bot.states import ChoiceAudio
from bot.support import get_current_time, on_error

group_id = os.getenv("GROUP_LOGS_ID")

try:
    @dp.message_handler(Text(equals="Отмена", ignore_case=True), state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        logger.info(f"Нажатие кнопки {message.text} при выборе аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при выборе аудио")
        await state.finish()
        await bot.send_message(message.chat.id, "Ты в главном меню", reply_markup=keyboards.main_menu)


    @dp.message_handler(text=["Выбрать категорию ✅", "Выбрать категорию", "выбрать категорию", "/choice_category"])
    async def choice_category(message: types.message):
        logger.info(f"Нажатие кнопки {message.text} при выборе аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при выборе аудио")
        await ChoiceAudio.start.set()
        await bot.send_message(
            message.chat.id,
            "Выберите категорию:",
            reply_markup=create_keyboard_category(db.read_category()),
            parse_mode=types.ParseMode.MARKDOWN,
        )


    @dp.message_handler(state=ChoiceAudio.start)
    async def choice_category(message: types.message, state: FSMContext):
        logger.info(f"Выбор категории {message.text} при выборе аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nВыбор категории {message.text} при выборе аудио")
        result = db.audio_for_category(message.text)
        await bot.send_message(
            message.chat.id,
            f"Вы выбрали категорию: {message.text}",
            reply_markup=keyboards.main_menu,
            parse_mode=types.ParseMode.MARKDOWN,
        )

        try:
            for name_file in result:
                await bot.send_audio(message.chat.id, audio=open(name_file, 'rb'))
        except FileNotFoundError:
            logger.error("FileNotFoundError  при выборе аудио")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nFileNotFoundError  при выборе аудио")
            await bot.send_message(
                message.chat.id,
                "Ошибка, аудио не найдено, попробуйте снова",
                reply_markup=keyboards.main_menu,
                parse_mode=types.ParseMode.MARKDOWN,
            )
        await state.finish()
except Exception as error:
    on_error("выборе", error)
