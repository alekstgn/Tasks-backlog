from __future__ import annotations

import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message

from database.db_manager import DatabaseManager
from utils.csv_generator import CSVGenerator
from utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


def _get_db_manager(message: Message) -> DatabaseManager | None:
    """
    Возвращает экземпляр DatabaseManager из контекста бота.

    Параметры:
        message (Message): сообщение, в рамках которого выполняется обработчик.

    Возвращает:
        Optional[DatabaseManager]: менеджер базы данных или None, если не найден.
    """
    return getattr(message.bot, "db_manager", None)


class TaskStates(StatesGroup):
    """
    Состояния для FSM (Finite State Machine).
    Используются для управления диалогом с пользователем.
    """

    waiting_for_task_text = State()  # Ожидание ввода текста задачи


@router.message(Command("add"))
async def cmd_add_task(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /add.
    Запрашивает у пользователя текст задачи.

    Логирует запуск команды на уровне INFO.
    """
    logger.info("Команда /add вызвана пользователем %s", message.from_user.id)

    await state.set_state(TaskStates.waiting_for_task_text)
    await message.answer("Введите текст задачи:")


@router.message(TaskStates.waiting_for_task_text)
async def process_task_text(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода текста задачи.
    Сохраняет задачу в базу данных и выводит подтверждение.

    Логирует добавление задачи на уровне INFO.
    """
    db = _get_db_manager(message)
    if db is None:
        logger.error("DatabaseManager не найден в контексте бота")
        await message.answer("Ошибка сервера: база данных недоступна.")
        await state.clear()
        return

    try:
        task_id = await db.add_task(message.text, message.from_user.id)
    except ValueError as error:
        logger.warning("Ошибка валидации при добавлении задачи: %s", error)
        await message.answer(str(error))
        return
    except Exception as error:  # pylint: disable=broad-except
        logger.exception("Не удалось добавить задачу: %s", error)
        await message.answer("Не удалось сохранить задачу. Попробуйте позже.")
        await state.clear()
        return

    logger.info(
        "Задача %s успешно добавлена для пользователя %s",
        task_id,
        message.from_user.id,
    )
    await state.clear()
    await message.answer("Задача сохранена ✅")


@router.message(Command("list"))
async def cmd_list_tasks(message: Message) -> None:
    """
    Обработчик команды /list.
    Выводит все задачи пользователя из базы данных.

    Если задач нет, выводит соответствующее сообщение.
    Логирует запрос списка задач на уровне INFO.
    """
    db = _get_db_manager(message)
    if db is None:
        logger.error("DatabaseManager не найден при выполнении /list")
        await message.answer("Ошибка сервера: база данных недоступна.")
        return

    try:
        tasks = await db.get_user_tasks(message.from_user.id)
    except Exception as error:  # pylint: disable=broad-except
        logger.exception("Не удалось получить список задач: %s", error)
        await message.answer("Не удалось получить список задач.")
        return

    if not tasks:
        await message.answer("У вас пока нет задач. Добавьте первую командой /add.")
        return

    lines = [
        f"{index}. {task.get_text()} (создана: {task.get_created_at()})"
        for index, task in enumerate(tasks, start=1)
    ]

    logger.info(
        "Пользователь %s запросил список задач (%s шт.)",
        message.from_user.id,
        len(tasks),
    )
    await message.answer("\n".join(lines))


@router.message(Command("list_csv"))
async def cmd_list_csv(message: Message) -> None:
    """
    Обработчик команды /list_csv.
    Генерирует CSV-файл с задачами и отправляет пользователю.

    Логирует генерацию и отправку CSV на уровне INFO.
    """
    db = _get_db_manager(message)
    if db is None:
        logger.error("DatabaseManager не найден при выполнении /list_csv")
        await message.answer("Ошибка сервера: база данных недоступна.")
        return

    try:
        tasks = await db.get_user_tasks(message.from_user.id)
    except Exception as error:  # pylint: disable=broad-except
        logger.exception("Не удалось получить задачи для CSV: %s", error)
        await message.answer("Не удалось подготовить CSV-файл.")
        return

    if not tasks:
        await message.answer("Нет задач для выгрузки. Добавьте их командой /add.")
        return

    try:
        file_path = CSVGenerator.generate_tasks_csv(tasks)
    except Exception as error:  # pylint: disable=broad-except
        logger.exception("Ошибка при генерации CSV: %s", error)
        await message.answer("Не удалось создать CSV-файл.")
        return

    logger.info(
        "Пользователю %s отправляется CSV-файл %s",
        message.from_user.id,
        file_path,
    )

    csv_file = FSInputFile(file_path)
    await message.answer_document(csv_file, caption="Задачи в формате CSV")

    try:
        os.remove(file_path)
    except OSError as error:
        logger.warning("Не удалось удалить временный CSV-файл: %s", error)

