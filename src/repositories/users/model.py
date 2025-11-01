from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from repositories.users.enum import UserRole
from src.repositories.core.base_model import BaseModel, TimestampsMixin


class User(BaseModel, TimestampsMixin):
    """Модель пользователей"""

    first_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, doc='Имя')
    last_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, doc='Фамилия')
    second_name: Mapped[str | None] = mapped_column(String(255), nullable=True, doc='Отчество')

    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False, doc='Электронная почта'
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False, doc='Пароль')

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False, default=UserRole.READER, doc='Уровень учетной записи'
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, doc='Учетная запись активна')
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, doc='Учетная запись суперпользователя'
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, doc='Учетная запись верифицирована'
    )
