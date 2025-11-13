import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from database.db_manager import DatabaseManager
from handlers import start_handler, task_handler
from utils.logger import setup_logger


async def main() -> None:
    """
    Главная функция приложения.

    Выполняет:
        1. Загрузку и валидацию конфигурации.
        2. Инициализацию логгера.
        3. Подключение к базе данных и создание таблиц.
        4. Инициализацию бота и диспетчера.
        5. Регистрацию роутеров.
        6. Запуск polling.

    Логирует все основные этапы на уровне INFO.
    """
    # Загружаем конфигурацию из переменных окружения
    Config.load_env()

    # Настраиваем центральный логгер и применяем уровень для модулей
    main_logger = setup_logger("taskbot", Config.LOG_LEVEL)
    setup_logger("database.db_manager", Config.LOG_LEVEL)
    setup_logger("handlers.start_handler", Config.LOG_LEVEL)
    setup_logger("handlers.task_handler", Config.LOG_LEVEL)
    setup_logger("utils.csv_generator", Config.LOG_LEVEL)

    main_logger.info("Запуск бота TaskBot")

    # Инициализируем менеджер базы данных и готовим таблицы
    db_manager = DatabaseManager(Config.DATABASE_PATH)
    await db_manager.connect()
    await db_manager.create_tables()

    # Создаем экземпляры бота и диспетчера
    bot = Bot(token=Config.BOT_TOKEN)
    setattr(bot, "db_manager", db_manager)  # Сохраняем менеджер как атрибут бота
    dispatcher = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры с обработчиками команд
    dispatcher.include_router(start_handler.router)
    dispatcher.include_router(task_handler.router)

    try:
        main_logger.info("Запуск процесса polling")
        await dispatcher.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        main_logger.info("Получен сигнал остановки. Завершение работы...")
    finally:
        await db_manager.close()
        await bot.session.close()
        main_logger.info("Бот остановлен корректно")


if __name__ == "__main__":
    asyncio.run(main())

