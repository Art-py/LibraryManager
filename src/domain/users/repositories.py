from typing import Protocol
from uuid import UUID

from src.domain.users.entities import User


class UserRepository(Protocol):
    """Коллекция пользователей, доступная прикладному слою."""

    async def get_by_uid(self, user_uid: UUID) -> User | None: ...

    async def get_by_email(self, user_email: str) -> User | None: ...

    async def add(self, user: User) -> User: ...
