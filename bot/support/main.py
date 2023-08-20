import datetime
import os
from bot.logger import logger

group_id = os.getenv("GROUP_LOGS_ID")
def get_current_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time
def on_error(state,error):
    logger.critical(f"При {state} аудио возникла ошибка: {error}")