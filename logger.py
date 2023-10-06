"""
Модуль logger предоставляет настройку и конфигурацию логирования с
использованием библиотеки loguru.
"""
from loguru import logger

# Логирование
logger.add(
    'debug.log',
    format='{time} {level} {message}',
    level='DEBUG',
    rotation='1 MB',
    compression='zip',
)
