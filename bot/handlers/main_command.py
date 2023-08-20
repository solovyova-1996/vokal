from aiogram import types

from bot import keyboards
from bot.loader import dp, bot
from bot.text import text
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Command


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, text["start_text"], reply_markup=keyboards.main_menu, parse_mode="HTML")


@dp.message_handler(commands=['menu'])
async def commands_menu(message: types.message):
    await bot.send_message(
        message.chat.id,
        "Ты в меню,выбери нужную команду",
        reply_markup=keyboards.main_menu,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(CommandHelp())
async def commands_menu(message: types.message):
    await bot.send_message(
        message.chat.id,
        text["help_text"],
        reply_markup=keyboards.main_menu,
        parse_mode=types.ParseMode.HTML,
    )


@dp.message_handler(commands=["Отмена"])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Ты в главном меню", reply_markup=keyboards.main_menu)
