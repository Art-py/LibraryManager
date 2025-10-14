import uuid

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(DeclarativeBase):
    """
    Базовый класс для моделей sqlAlchemy
    """

    __abstract__ = True

    uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)


class CreatedAtMixin:
    """
    Добавляет created_at с временем создания
    """

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class UpdatedAtMixin:
    """
    Добавляет updated_at с временем обновления
    """

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class TimestampsMixin(CreatedAtMixin, UpdatedAtMixin):
    """
    Добавляет created_at и updated_at с временем создания/обновления
    """

    pass
