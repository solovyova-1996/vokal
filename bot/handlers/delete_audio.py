import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot import keyboards
from bot.keyboards.buttons import create_keyboard_category
from bot.loader import dp, bot, db
from bot.logger import logger
from bot.states import DeleteAudio
from bot.support import get_current_time, on_error

group_id = os.getenv("GROUP_LOGS_ID")

try:
    @dp.message_handler(Text(equals="Отмена", ignore_case=True), state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        logger.info(f"Нажатие кнопки {message.text} при удалении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при удалении аудио")
        await state.finish()
        await bot.send_message(message.chat.id, "Ты в главном меню", reply_markup=keyboards.main_menu)


    @dp.message_handler(text=["Удалить ❌", "Удалить", "удалить", "/delete"])
    async def add_name(message: types.message):
        logger.info(f"Нажатие кнопки {message.text} при удалении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при удалении аудио")
        await DeleteAudio.start.set()
        await bot.send_message(
            message.chat.id,
            "Выбери аудио для удаления",
            reply_markup=keyboards.create_all_audio(db.read_json_file()),
            parse_mode=types.ParseMode.MARKDOWN,
        )


    @dp.message_handler(state=DeleteAudio.start)
    async def name_add(message: types.Message, state: FSMContext):
        logger.info(f"Переход в состояние start {message.text} при удалении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние start {message.text} при удалении аудио")
        await DeleteAudio.next()
        async with state.proxy() as data:
            data["name"] = message.text

        await bot.send_message(
            message.chat.id, f" Вы хотите удалить аудио:\n {message.text}", reply_markup=keyboards.yes_or_no)


    @dp.message_handler(state=DeleteAudio.end)
    async def delete_end(message: types.Message, state: FSMContext):
        logger.info(f"Переход в состояние end {message.text} при удалении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние end {message.text} при удалении аудио")
        async with state.proxy() as data:
            name = data["name"].split("|")[0].split(":")[-1]
        if message.text == "Да":
            logger.info(f"Удаление аудио: {name}")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nУдаление аудио: {name}")
            await state.finish()
            db.delete_item_from_json(name.lstrip().rstrip())

            await bot.send_message(
                message.chat.id, "Аудио удалено", reply_markup=keyboards.main_menu)
        else:
            logger.info(f"Аудио не удалено: {name}")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nАудио не удалено: {name}")
            await state.finish()
            await bot.send_message(
                message.chat.id, "Аудио не удалено", reply_markup=keyboards.main_menu)
except Exception as error:
    on_error("удалении", error)
