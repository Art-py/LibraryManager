from src.repositories.core.base_uow import BaseUOW
from src.repositories.users.uow_mixin import UserUOWMixin


class UserUOW(BaseUOW, UserUOWMixin):
    """UOW пользователя"""
