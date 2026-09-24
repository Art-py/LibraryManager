from uuid import UUID

from src.application.common.unit_of_work import UnitOfWork
from src.application.users.errors import UserNotFoundError
from src.domain.users.entities import User


class GetUserService:
    """Возвращает пользователя по идентификатору."""

    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def execute(self, user_uid: UUID) -> User:
        user = await self._unit_of_work.users.get_by_uid(user_uid)
        if user is None:
            raise UserNotFoundError('User not found')
        return user
