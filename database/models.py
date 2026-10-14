import datetime
from sqlalchemy import BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    # Telegram ID делаем BigInteger, так как они давно вышли за пределы стандартного int
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    registered_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    
    # Связь "один ко многим" с обращениями
    complaints: Mapped[list["Complaint"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Complaint(Base):
    __tablename__ = "complaints"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"))
    issue_type: Mapped[str] = mapped_column(String(100))  # Например: "Таза Қазақстан" или "Коррупция"
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    ai_resolution: Mapped[str] = mapped_column(Text, nullable=True) # Что ответил ИИ со ссылкой на Конституцию 2026
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    
    user: Mapped["User"] = relationship(back_populates="complaints")
