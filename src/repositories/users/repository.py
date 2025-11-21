from uuid import UUID

from sqlalchemy import select

from src.repositories.core.base_repository_model import BaseRepository
from src.repositories.core.exceptions.http_exceptions import NotFoundException
from src.repositories.users.model import User


class UserRepository(BaseRepository):
    """Репозиторий пользователя"""

    async def get_by_uid(self, user_uid: UUID) -> User | None:
        """Получить пользователя по UID"""
        result = await self._session.execute(select(User).where(User.uid == user_uid))
        user = result.scalar_one_or_none()
        if user is None:
            raise NotFoundException(message='User not found')
        return user

    async def get_by_email(self, user_email: str) -> User | None:
        """Получить пользователя по email"""
        result = await self._session.execute(select(User).where(User.email == user_email))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Создание пользователя"""
        self._session.add(user)
        return user
