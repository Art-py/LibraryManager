from fastapi import Depends

from src.domains.users.enum import UserRole
from src.domains.users.exception import UserIsRegistered
from src.domains.users.model import User
from src.domains.users.schema import UserCreate
from src.domains.users.security import get_hashed_password
from src.domains.users.uow import UserUOW


class CreateUserHandler:
    """Хэндлер для создания пользователя"""

    def __init__(self, unit: UserUOW):
        self.unit = unit
        self.repository = self.unit.get_user_repository()

    @classmethod
    async def get_dependency(cls, unit: UserUOW = Depends(UserUOW.get_dependency)):
        return cls(unit=unit)

    async def handle(self, user_data: UserCreate) -> User:
        user = await self.repository.get_by_email(user_email=user_data.email)
        if user is not None:
            raise UserIsRegistered('User is already registered')

        data = user_data.model_dump()

        data.pop('password', None)
        data['hashed_password'] = await get_hashed_password(data.pop('password_confirm', None))

        data['role'] = UserRole.READER

        data['is_active'] = False
        data['is_superuser'] = False
        data['is_verified'] = True  # TODO переделать на False когда реализую логику верификации аккаунта

        user = await self.repository.create(user=User(**data))
        await self.unit.commit()

        return user
