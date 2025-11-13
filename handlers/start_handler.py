from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """
    Обработчик команды /start.
    Приветствует пользователя и выводит список доступных команд.

    Логирует запуск команды на уровне INFO.
    """
    logger.info("Команда /start вызвана пользователем %s", message.from_user.id)

    greeting = (
        "Привет! Я бот для хранения задач.\n\n"
        "Доступные команды:\n"
        "/add — добавить новую задачу\n"
        "/list — показать ваши задачи\n"
        "/list_csv — получить задачи в формате CSV"
    )
    await message.answer(greeting)

