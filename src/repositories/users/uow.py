from repositories.core.base_uow import BaseUOW
from repositories.users.uow_mixin import UserUOWMixin


class UserUOW(BaseUOW, UserUOWMixin):
    """UOW пользователя"""
