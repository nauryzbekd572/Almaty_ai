import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    if not TELEGRAM_TOKEN:
        raise ValueError("Критическая ошибка: TELEGRAM_TOKEN не задан в .env файле!")

settings = Settings()
