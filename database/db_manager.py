from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import aiosqlite

from database.models import Task
from utils.logger import setup_logger


class DatabaseManager:
    """
    Менеджер для работы с базой данных SQLite.
    Отвечает за подключение, создание таблиц и выполнение CRUD операций.
    """

    def __init__(self, db_path: str):
        """
        Конструктор класса DatabaseManager.

        Параметры:
            db_path (str): путь к файлу базы данных.
        """
        self._db_path = db_path
        self._connection: Optional[aiosqlite.Connection] = None
        self._logger = setup_logger(__name__)

    async def connect(self) -> None:
        """
        Устанавливает соединение с базой данных.
        Логирует успешное подключение на уровне INFO.
        """
        if self._connection is not None:
            return

        # Создаем асинхронное соединение с базой данных
        self._connection = await aiosqlite.connect(self._db_path)
        self._connection.row_factory = aiosqlite.Row
        await self._connection.execute("PRAGMA foreign_keys = ON;")
        await self._connection.commit()

        self._logger.info("Установлено соединение с базой данных %s", self._db_path)

    async def create_tables(self) -> None:
        """
        Создает таблицу tasks, если она не существует.

        Структура таблицы:
            - id: INTEGER PRIMARY KEY AUTOINCREMENT
            - text: TEXT NOT NULL
            - user_id: INTEGER NOT NULL
            - created_at: TEXT NOT NULL (дата в формате ISO 8601)

        Логирует создание таблицы на уровне INFO.
        """
        if self._connection is None:
            await self.connect()
        assert self._connection is not None

        await self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        await self._connection.commit()

        self._logger.info("Таблица tasks проверена/создана")

    async def add_task(self, text: str, user_id: int) -> int:
        """
        Добавляет новую задачу в базу данных.

        Параметры:
            text (str): текст задачи.
            user_id (int): ID пользователя Telegram.

        Возвращает:
            int: ID добавленной задачи.

        Логирует добавление задачи на уровне INFO.
        """
        if self._connection is None:
            await self.connect()
        assert self._connection is not None

        # Валидация и подготовка данных к сохранению
        if not text or len(text.strip()) == 0:
            raise ValueError("Текст задачи не может быть пустым")

        clean_text = text.strip()
        created_at = datetime.now().isoformat()

        cursor = await self._connection.execute(
            "INSERT INTO tasks (text, user_id, created_at) VALUES (?, ?, ?);",
            (clean_text, user_id, created_at),
        )
        await self._connection.commit()

        task_id = cursor.lastrowid
        await cursor.close()

        self._logger.info(
            "Задача ID %s добавлена для пользователя %s", task_id, user_id
        )
        return task_id

    async def get_user_tasks(self, user_id: int) -> List[Task]:
        """
        Получает все задачи пользователя из базы данных.

        Параметры:
            user_id (int): ID пользователя Telegram.

        Возвращает:
            list[Task]: Список объектов Task.

        Логирует количество найденных задач на уровне INFO.
        """
        if self._connection is None:
            await self.connect()
        assert self._connection is not None

        cursor = await self._connection.execute(
            "SELECT id, text, user_id, created_at FROM tasks "
            "WHERE user_id = ? ORDER BY datetime(created_at) ASC;",
            (user_id,),
        )
        rows = await cursor.fetchall()
        await cursor.close()

        tasks = [
            Task(
                task_id=row["id"],
                text=row["text"],
                user_id=row["user_id"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

        self._logger.info(
            "Получено %s задач для пользователя %s", len(tasks), user_id
        )
        return tasks

    async def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        Логирует закрытие соединения на уровне INFO.
        """
        if self._connection is None:
            return

        await self._connection.close()
        self._connection = None
        self._logger.info("Соединение с базой данных закрыто")

