from abc import ABC

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session


class BaseRepository(ABC):
    """Базовая модель для репозиториев"""

    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @classmethod
    async def get_dependency(cls, session: AsyncSession = Depends(get_async_session)):
        return cls(session=session)
