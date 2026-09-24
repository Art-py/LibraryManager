from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.entities import User
from src.infrastructure.database.mappers.user import UserMapper
from src.infrastructure.database.models.user import UserRecord


class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_uid(self, user_uid: UUID) -> User | None:
        result = await self._session.execute(select(UserRecord).where(UserRecord.uid == user_uid))
        record = result.scalar_one_or_none()
        return UserMapper.to_domain(record) if record is not None else None

    async def get_by_email(self, user_email: str) -> User | None:
        result = await self._session.execute(select(UserRecord).where(UserRecord.email == user_email))
        record = result.scalar_one_or_none()
        return UserMapper.to_domain(record) if record is not None else None

    async def add(self, user: User) -> User:
        self._session.add(UserMapper.to_record(user))
        return user
