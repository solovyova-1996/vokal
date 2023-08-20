import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot import keyboards
from bot.keyboards.buttons import create_keyboard_category
from bot.loader import dp, bot, db
from bot.logger import logger
from bot.states import AddAudio
from bot.support import get_current_time, on_error
from aiogram.dispatcher.filters.builtin import Command

group_id = os.getenv("GROUP_LOGS_ID")
try:

    @dp.message_handler(Text(equals="Отмена", ignore_case=True), state="*")
    async def cancel_handler(message: types.Message, state: FSMContext):
        logger.info(f"Нажатие кнопки {message.text} при добавлении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при добавлении аудио")
        await state.finish()
        await bot.send_message(message.chat.id, "Ты в главном меню", reply_markup=keyboards.main_menu)


    @dp.message_handler(text=["Загрузить ⬇", "Загрузить", "загрузить", "/download"])
    async def add_name(message: types.message):
        logger.info(f"Нажатие кнопки {message.text} при добавлении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при добавлении аудио")
        await AddAudio.name.set()
        await bot.send_message(
            message.chat.id,
            "Напиши название аудио",
            reply_markup=keyboards.cancel_markup,
            parse_mode=types.ParseMode.MARKDOWN,
        )


    @dp.message_handler(state=AddAudio.name)
    async def name_add(message: types.Message, state: FSMContext):
        logger.info("Переход в состояние добавления имени при добавлении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние добавления имени при добавлении аудио")
        result = db.check_name(message.text.rstrip().lstrip())
        if result:
            logger.info("Выбрано имя которое уже существует")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nВыбрано имя которое уже существует:{message.text}")

            await bot.send_message(
                message.chat.id, f"Имя {message.text} уже существует\nПридумайте другое",
                reply_markup=keyboards.cancel_markup)
            await AddAudio.name.set()

        else:
            logger.info("Выбрано имя ")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nВыбрано имя:{message.text}")
            await AddAudio.next()
            async with state.proxy() as data:
                data["name"] = message.text
            await bot.send_message(
                message.chat.id,
                "Имя добавлено,теперь добавьте аудио\nНажми на значок скрепочки 📎,\nчтобы выбрать и отправить файл",
                reply_markup=keyboards.cancel_markup)


    @dp.message_handler(state=AddAudio.start, content_types=types.ContentType.AUDIO)
    async def handle_audio(message: types.Message, state: FSMContext):
        logger.info("Переход в состояние загрузки файла при добавлении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние загрузки файла при добавлении аудио")

        async with state.proxy() as data:
            name = data["name"]
            data["params"] = []
        audio = message.audio
        file_id = audio.file_id
        file = await bot.get_file(file_id)

        audio_path = os.path.join("src", f'audio_{name}.mp3')
        audio_data = await file.download(audio_path)
        await AddAudio.next()
        await bot.send_message(
            message.chat.id,
            "Спасибо за аудиозапись! \nТеперь добавь параметр\nНапиши один параметр и дождись следующего сообщения от меня",
            reply_markup=create_keyboard_category(db.read_category()))
        async with state.proxy() as data:
            data["file"] = audio_path


    @dp.message_handler(state=AddAudio.param_1)
    async def param_add(message: types.Message, state: FSMContext):
        logger.info("Переход в состояние добавления первого параметра при добавлении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние добавления первого параметра при добавлении аудио:{message.text}")
        async with state.proxy() as data:
            data["params"].append(message.text)
        await bot.send_message(
            message.chat.id, "Параметр добавлен,хотите добавить еще, или закончить добавлени параметров?",
            reply_markup=keyboards.intermediate_keyboard)

        await AddAudio.next()


    @dp.message_handler(state=AddAudio.param_2)
    async def param_add(message: types.Message, state: FSMContext):
        logger.info("Переход в состояние добавления второго параметра при добавлении аудио")
        await bot.send_message(group_id,
                               f"{get_current_time()}\n{message.from_user.id}\nПереход в состояние добавления второго параметра при добавлении аудио")
        if message.text == "Добавить ещё":
            logger.info(f"Нажатие на кнопку {message.text} при добавлении аудио")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при добавлении аудио")

            await AddAudio.param_1.set()
            await bot.send_message(
                message.chat.id, "Добавь параметр\nНапиши один параметр и дождись следующего сообщения от меня",
                reply_markup=create_keyboard_category(db.read_category()))
        elif message.text == "Закончить":
            logger.info(f"Нажатие на кнопку {message.text} при добавлении аудио")
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nНажатие кнопки {message.text} при добавлении аудио")

            result = {}
            async with state.proxy() as data:
                result['name'] = data['name']
                result['params'] = data['params']
                result['file'] = data['file']
            db.append_to_json(result)
            await state.finish()
            await bot.send_message(
                message.chat.id, "Аудиозапись добавлена 🎵",
                reply_markup=keyboards.main_menu)
            await bot.send_message(group_id,
                                   f"{get_current_time()}\n{message.from_user.id}\nАудиозапись добавлена")

except Exception as error:
    on_error("добавлении", error)
