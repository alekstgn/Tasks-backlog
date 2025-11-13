import logging
from typing import Optional


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Настраивает и возвращает логгер для модуля.

    Параметры:
        name (str): имя логгера (обычно __name__).
        level (str): уровень логирования (по умолчанию INFO).

    Возвращает:
        logging.Logger: настроенный объект Logger.

    Формат логов: [ВРЕМЯ] [УРОВЕНЬ] [МОДУЛЬ] - СООБЩЕНИЕ.
    """
    logger = logging.getLogger(name)

    # Преобразование уровня логирования в объект logging
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Проверяем, добавлен ли уже обработчик, чтобы избежать дублирования сообщений
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

