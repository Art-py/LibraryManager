from sqlalchemy.ext.asyncio import AsyncSession


class BaseUOWMixin:
    """Базовый класс миксина, в нем получаем репозитории с которыми планируем работать"""

    session: AsyncSession
