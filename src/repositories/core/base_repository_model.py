from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    """Базовая модель для репозиториев"""

    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
