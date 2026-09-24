from uuid import UUID

import uuid6
from sqlalchemy import Boolean, Enum, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.users.enums import UserRole
from src.infrastructure.database.base import OrmBase, TimestampMixin


class UserRecord(OrmBase, TimestampMixin):
    """SQLAlchemy-представление таблицы пользователей."""

    __tablename__ = 'users'

    uid: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid6.uuid7,
        doc='Внутренний идентификатор',
    )
    first_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, doc='Имя')
    last_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, doc='Фамилия')
    second_name: Mapped[str | None] = mapped_column(String(255), nullable=True, doc='Отчество')
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False, doc='Электронная почта'
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False, doc='Пароль')
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name='userrole'),
        nullable=False,
        default=UserRole.READER,
        doc='Уровень учетной записи',
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, doc='Учетная запись активна')
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, doc='Учетная запись суперпользователя'
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, doc='Учетная запись верифицирована'
    )
