from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database.models import Base

DATABASE_URL = "sqlite+aiosqlite:///./adal_qogam.db"

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=False)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Инициализация таблиц в БД (вызываем при старте бота)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
