from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from repositories.users.enum import UserRole
from src.repositories.core.base_model import BaseModel, TimestampsMixin

class User(BaseModel, TimestampsMixin):
    """Модель пользователей"""

    __tablename__ = 'users'

    first_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    second_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.READER)
