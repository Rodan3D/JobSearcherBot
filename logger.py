from loguru import logger


# Логирование
logger.add(
    "debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 MB",
    compression="zip",
)
