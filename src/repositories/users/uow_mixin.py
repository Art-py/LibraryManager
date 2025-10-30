from repositories.core.base_uow_mixin import BaseUOWMixin
from repositories.users.repository import UserRepository


class UserUOWMixin(BaseUOWMixin):
    """Миксин uow пользователя для получения репозиториев"""

    async def get_user_repository(self) -> UserRepository:
        """Получить репозиторий пользователя"""
        return UserRepository(self.session)
