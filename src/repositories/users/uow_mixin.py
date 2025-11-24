from src.repositories.core.base_uow_mixin import BaseUOWMixin
from src.repositories.users.repository import UserRepository


class UserUOWMixin(BaseUOWMixin):
    """Миксин uow пользователя для получения репозиториев"""

    def get_user_repository(self) -> UserRepository:
        """Получить репозиторий пользователя"""
        return UserRepository(self.session)
