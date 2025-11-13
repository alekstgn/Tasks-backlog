from __future__ import annotations

from datetime import datetime
from typing import Optional


class Task:
    """
    Класс для представления задачи.
    Содержит информацию о тексте задачи, пользователе и времени создания.
    """

    def __init__(self, task_id: int, text: str, user_id: int, created_at: str):
        """
        Конструктор класса Task.

        Параметры:
            task_id (int): уникальный идентификатор задачи
            text (str): текст задачи
            user_id (int): ID пользователя Telegram
            created_at (str): дата и время создания задачи в формате ISO 8601
        """
        self._id = task_id
        self._text = text
        self._user_id = user_id
        self._created_at = created_at

    def get_id(self) -> int:
        """Возвращает ID задачи."""
        return self._id

    def get_text(self) -> str:
        """Возвращает текст задачи."""
        return self._text

    def get_user_id(self) -> int:
        """Возвращает ID пользователя."""
        return self._user_id

    def get_created_at(self) -> str:
        """Возвращает дату создания задачи."""
        return self._created_at

    def set_text(self, new_text: str) -> None:
        """
        Изменяет текст задачи.

        Параметры:
            new_text (str): новый текст задачи.

        Исключения:
            ValueError: если новый текст пустой.
        """
        # Проверяем, что текст задачи содержит хотя бы один символ
        if not new_text or len(new_text.strip()) == 0:
            raise ValueError("Текст задачи не может быть пустым")
        self._text = new_text

    def __str__(self) -> str:
        """Возвращает строковое представление задачи."""
        return (
            f"Задача #{self._id}: '{self._text}' "
            f"(пользователь: {self._user_id}, создана: {self._created_at})"
        )


class User:
    """
    Класс для представления пользователя бота.
    Подходит для расширения функциональности в будущем.
    """

    def __init__(self, user_id: int, username: Optional[str] = None):
        """
        Конструктор класса User.

        Параметры:
            user_id (int): уникальный идентификатор пользователя Telegram.
            username (Optional[str]): никнейм пользователя, если доступен.
        """
        self._user_id = user_id
        self._username = username or ""
        self._registered_at = datetime.now().isoformat()

    def get_user_id(self) -> int:
        """Возвращает ID пользователя."""
        return self._user_id

    def get_username(self) -> str:
        """Возвращает никнейм пользователя."""
        return self._username

    def get_registered_at(self) -> str:
        """Возвращает дату регистрации пользователя в системе."""
        return self._registered_at

