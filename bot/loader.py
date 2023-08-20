import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.db_work.main import DbWork

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DbWork("db.json")
