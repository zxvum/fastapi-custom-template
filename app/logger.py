from loguru import logger
from termcolor import colored
import sys

# Конфигурируем Loguru для вывода логов в консоль
logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>", colorize=True, level="INFO")

# Функция для логирования ошибок с цветом
def log_error(message):
    error_message = colored(message, "red")
    logger.error(error_message)