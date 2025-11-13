import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv, find_dotenv


class Config:
    """
    Класс для управления конфигурацией приложения.
    Загружает переменные окружения и предоставляет доступ к настройкам.
    """

    BOT_TOKEN: str = ""
    DATABASE_PATH: str = "./tasks.db"
    LOG_LEVEL: str = "INFO"

    @classmethod
    def load_env(cls, env_file: str = ".env") -> None:
        """
        Загружает переменные из .env файла и сохраняет их в атрибутах класса.

        Параметры:
            env_file (str): Путь к файлу с переменными окружения.

        Исключения:
            ValueError: Если обязательные параметры не указаны.
        """
        # Определяем путь к файлу .env относительно текущего файла конфигурации
        config_dir = Path(__file__).resolve().parent
        env_path = config_dir / env_file

        # Если .env не найден рядом с проектом, пробуем стандартный поиск
        if not env_path.exists():
            found_path = find_dotenv(filename=env_file)
            if found_path:
                env_path = Path(found_path)

        # Загрузка значений из найденного .env файла и системных переменных
        load_dotenv(env_path)

        # Считывание значений с удалением лишних пробелов
        cls.BOT_TOKEN = (os.getenv("BOT_TOKEN") or "").strip()
        cls.DATABASE_PATH = (os.getenv("DATABASE_PATH") or "./tasks.db").strip()
        cls.LOG_LEVEL = (os.getenv("LOG_LEVEL") or "INFO").strip().upper()

        # Валидация обязательных параметров конфигурации
        cls.validate()

    @classmethod
    def validate(cls) -> None:
        """
        Проверяет наличие обязательных параметров конфигурации.

        Исключения:
            ValueError: Если обнаружены отсутствующие параметры.
        """
        # Формирование списка обязательных параметров без значений
        missing: List[str] = []
        if not cls.BOT_TOKEN:
            missing.append("BOT_TOKEN")
        if not cls.DATABASE_PATH:
            missing.append("DATABASE_PATH")

        # Генерация исключения с перечислением отсутствующих параметров
        if missing:
            raise ValueError(
                f"Отсутствуют обязательные параметры конфигурации: {', '.join(missing)}"
            )

