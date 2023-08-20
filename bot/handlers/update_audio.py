import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot import keyboards
from bot.keyboards.buttons import create_keyboard_category
from bot.loader import dp, bot, db
from bot.logger import logger
from bot.states import UpdateAudio
from bot.support import on_error, get_current_time

group_id = os.getenv("GROUP_LOGS_ID")
try:
    @dp.message_handler(Text(equals="Отмена", ignore_case=True), state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        logger.info(f"Нажатие кнопки {message.text} при выборе аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при выборе аудио")
        await state.finish()
        await bot.send_message(message.chat.id, "Ты в главном меню", reply_markup=keyboards.main_menu)


    @dp.message_handler(text=["Изменить", "изменить", "Изменить ✏", "/update"])
    async def update_audio(message: types.message):
        logger.info(f"Нажатие кнопки {message.text} при выборе аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при выборе аудио")
        await UpdateAudio.start.set()

        await bot.send_message(
            message.chat.id,
            "Выбери аудио для изменения",
            reply_markup=keyboards.create_all_audio(db.read_json_file()),
            parse_mode=types.ParseMode.MARKDOWN,
        )


    @dp.message_handler(state=UpdateAudio.start)
    async def start_update_audio(message: types.message, state: FSMContext):
        logger.info(f"Переход в состояние start {message.text} при изменении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние start {message.text} при изменении аудио")
        await UpdateAudio.param_1.set()
        async with state.proxy() as data:
            data["params"] = []
            data["name"] = message.text

        await bot.send_message(
            message.chat.id, "Теперь добавь параметры\nПредыдущие параметры аудио удаляться",
            reply_markup=create_keyboard_category(db.read_category()))


    @dp.message_handler(state=UpdateAudio.param_1)
    async def param_add(message: types.Message, state: FSMContext):
        logger.info(f"Переход в состояние param_1 {message.text} при изменении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние param_1 {message.text} при изменении аудио")

        async with state.proxy() as data:
            data["params"].append(message.text)
        await bot.send_message(
            message.chat.id, "Параметр добавлен,хотите добавить еще, или закончить добавлени параметров?",
            reply_markup=keyboards.intermediate_keyboard)

        await UpdateAudio.next()


    @dp.message_handler(state=UpdateAudio.param_2)
    async def param_add(message: types.Message, state: FSMContext):
        logger.info(f"Переход в состояние param_2 {message.text} при изменении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние param_2 {message.text} при изменении аудио")

        if message.text == "Добавить ещё":
            logger.info(f"Нажатие кнопки {message.text} при выборе аудио")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при выборе аудио")
            await UpdateAudio.param_1.set()
            await bot.send_message(
                message.chat.id, "добавьте параметры",
                reply_markup=create_keyboard_category(db.read_category()))
        elif message.text == "Закончить":
            logger.info(f"Нажатие кнопки {message.text} при выборе аудио")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при выборе аудио")
            result = {}
            async with state.proxy() as data:
                print(data)

                name = data["name"].split("|")[0].split(":")[-1].rstrip().lstrip()
                result = data['params']

            db.update_params_by_name(name, result)
            await state.finish()
            await bot.send_message(
                message.chat.id, "Параметры изменены",
                reply_markup=keyboards.main_menu)
except Exception as error:
    on_error("обновлении", error)
