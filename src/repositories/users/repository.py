from uuid import UUID

from sqlalchemy import select

from repositories.core.base_repository_model import BaseRepository
from repositories.users.model import User


class UserRepository(BaseRepository):
    """Репозиторий пользователя"""

    async def get_by_uid(self, user_uid: UUID) -> User | None:
        """Получить пользователя по UID"""
        result = await self._session.execute(select(User).where(User.uid == user_uid))
        return result.scalar_one_or_none()

    async def get_by_email(self, user_email: str) -> User | None:
        """Получить пользователя по email"""
        result = await self._session.execute(select(User).where(User.email == user_email))
        return result.scalar_one_or_none()
