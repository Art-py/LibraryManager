from src.domains.core.base_uow import BaseUOW
from src.domains.users.uow_mixin import UserUOWMixin


class UserUOW(BaseUOW, UserUOWMixin):
    """UOW пользователя"""
