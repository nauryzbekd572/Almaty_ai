import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from config.settings import settings
from database.base import init_db
from handlers.complaints import router as complaints_router

async def main():
    # Настраиваем логирование для отладки на хакатоне
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout
    )

    # Инициализируем таблицы БД асинхронно перед запуском бота
    logging.info("Инициализация базы данных...")
    await init_db()

    # Инициализация бота и диспетчера
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    dp = Dispatcher()

    # Подключаем роутер с нашей бизнес-логикой
    dp.include_router(complaints_router)

    logging.info("Бот успешно запущен и готов к работе!")
    
    # Запуск пуллинга (пропускаем накопленные апдейты для стабильности на защите)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
