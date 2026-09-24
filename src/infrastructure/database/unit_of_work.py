from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.errors import translate_integrity_error
from src.infrastructure.database.repositories.user import SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.users = SqlAlchemyUserRepository(session)

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except IntegrityError as error:
            await self._session.rollback()
            raise translate_integrity_error(error) from error

    async def rollback(self) -> None:
        await self._session.rollback()
