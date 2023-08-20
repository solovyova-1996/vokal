import os

from aiogram.utils import executor
from bot.handlers import dp

from bot.loader import bot
from bot.logger import logger
from bot.support import get_current_time

group_id = os.getenv("GROUP_LOGS_ID")


async def on_startup(_):
    print('Bot online')
    await bot.send_message(group_id,f"{get_current_time()}\nБот запущен")
    logger.info("Бот запущен")
    await bot.send_message("1454049968", "Бот запущен и готов к работе")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
