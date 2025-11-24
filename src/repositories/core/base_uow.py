from abc import ABC

from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.repositories.utils.db_error_mapper import map_integrity_error


class BaseUOW(ABC):
    """
    Базовый класс UOW содержит в себе методы для управления транзакциями
    """

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    async def get_dependency(cls, session: AsyncSession = Depends(get_async_session)):
        return cls(session=session)

    async def flash(self):
        """Применяет все накопленные изменения в транзакции, данное действие можно откатить"""
        try:
            await self.session.flush()
        except IntegrityError as e:
            raise map_integrity_error(e) from e

    async def commit(self):
        """Применяет все накопленные изменения в транзакции, данное действие невозможно откатить"""
        try:
            await self.session.commit()
        except IntegrityError as e:
            raise map_integrity_error(e) from e

    async def rollback(self):
        """Откат изменений"""
        await self.session.rollback()
