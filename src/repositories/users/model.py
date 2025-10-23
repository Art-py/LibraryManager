from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from repositories.users.enum import UserRole
from src.repositories.core.base_model import BaseModel, TimestampsMixin

from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class User(BaseModel, SQLAlchemyBaseUserTableUUID, TimestampsMixin):
    """Модель пользователей"""

    first_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    second_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.READER)
