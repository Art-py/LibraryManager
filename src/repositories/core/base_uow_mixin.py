from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class BaseUOWMixin(ABC):
    """Базовый класс миксина, в нем получаем репозитории с которыми планируем работать"""

    session: AsyncSession
