import logging

# Создаем объект логгера
logger = logging.getLogger("bot_logger")
logger.setLevel(logging.INFO)

# Создаем обработчик для сохранения логов в файл
file_handler = logging.FileHandler("bot_log_file.log",encoding='utf-8')

# Устанавливаем уровень логирования для обработчика
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер для определения структуры логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем обработчик в логгер
logger.addHandler(file_handler)

# Примеры использования логгера
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")










