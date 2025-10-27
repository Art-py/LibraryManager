import uuid

import uuid6
from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.repositories.utils.utils import camel_case_to_snake_case

CONVENTION = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


class BaseModel(DeclarativeBase):
    """Базовый класс для моделей sqlAlchemy"""

    __abstract__ = True

    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7, doc='Внутренний идентификатор'
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{camel_case_to_snake_case(cls.__name__)}s'

    metadata = MetaData(naming_convention=CONVENTION)


class CreatedAtMixin:
    """Добавляет created_at с временем создания"""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class UpdatedAtMixin:
    """Добавляет updated_at с временем обновления"""

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class TimestampsMixin(CreatedAtMixin, UpdatedAtMixin):
    """Добавляет created_at и updated_at с временем создания/обновления"""

    pass
