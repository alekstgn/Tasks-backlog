# TaskBot — Telegram-бот для управления задачами

Минимально работающий бот для хранения задач с использованием Python, aiogram 3.x и SQLite3.

## Функциональность

- `/start` — приветствие и список команд.
- `/add` — добавление новой задачи.
- `/list` — вывод всех задач пользователя.
- `/list_csv` — выгрузка задач в CSV.

## Установка

1. Клонируй репозиторий и перейди в директорию `TaskBot`.
2. Установи зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Скопируй `.env.example` в `.env` и укажи токен бота.
4. Запусти бота:

   ```bash
   python main.py
   ```

## Структура проекта

```
TaskBot/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
├── database/
│   ├── __init__.py
│   ├── models.py
│   └── db_manager.py
├── handlers/
│   ├── __init__.py
│   ├── start_handler.py
│   └── task_handler.py
├── keyboards/
│   ├── __init__.py
│   └── reply_keyboards.py
└── utils/
    ├── __init__.py
    ├── logger.py
    └── csv_generator.py
```

## Технологии

- Python 3.11+
- aiogram 3.x
- SQLite3
- aiosqlite

