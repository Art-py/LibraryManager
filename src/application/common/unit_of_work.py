from typing import Protocol

from src.domain.users.repositories import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
