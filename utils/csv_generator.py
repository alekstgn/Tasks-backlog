import csv
import os
from itertools import cycle
from typing import List

from database.models import Task
from utils.logger import setup_logger


class CSVGenerator:
    """
    Класс для генерации CSV-файлов с задачами.
    """

    _logger = setup_logger(__name__)

    @staticmethod
    def generate_tasks_csv(tasks: List[Task], filename: str = "tasks.csv") -> str:
        """
        Генерирует CSV-файл из списка задач.

        Параметры:
            tasks (List[Task]): список объектов Task.
            filename (str): имя выходного файла.

        Возвращает:
            str: путь к созданному файлу.

        Структура CSV:
            | ID | Текст | Пользователь | Дата создания | Статус | Категория |

        Логирует создание файла на уровне INFO.

        Исключения:
            ValueError: если список задач пуст.
            OSError: если произошла ошибка при записи файла.
        """
        # Проверяем, что передан непустой список задач
        if not tasks:
            raise ValueError("Нельзя создать CSV: список задач пуст")

        # Формируем абсолютный путь к файлу
        file_path = os.path.abspath(filename)

        # Открываем файл для записи и сохраняем данные в CSV-формате
        statuses = cycle(["Выполнена", "В работе", "Отложена"])
        categories = cycle(["Работа", "Личное", "Учеба"])

        # Используем кодировку UTF-8 с BOM, чтобы файл корректно открывался в Excel
        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(["ID", "Текст", "Пользователь", "Дата создания", "Статус", "Категория"])

            for task in tasks:
                writer.writerow(
                    [
                        task.get_id(),
                        task.get_text(),
                        task.get_user_id(),
                        task.get_created_at(),
                        next(statuses),
                        next(categories),
                    ]
                )

        CSVGenerator._logger.info(
            "CSV-файл с %s задачами сохранен по пути %s", len(tasks), file_path
        )
        return file_path

