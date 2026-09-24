import pytest
import pytest_asyncio
import uuid6
from faker.proxy import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.entities import User
from src.domain.users.enums import UserRole
from src.infrastructure.database.repositories.user import SqlAlchemyUserRepository
from test.core.factories.user import UserFactory

faker = Faker(locale='ru')


@pytest_asyncio.fixture
async def repository(sql_test_session: AsyncSession) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(sql_test_session)


class TestSqlAlchemyUserRepository:
    @pytest.mark.asyncio
    async def test_get_by_uid(self, repository: SqlAlchemyUserRepository, user: User):
        assert await repository.get_by_uid(user.uid) == user

    @pytest.mark.asyncio
    async def test_get_by_uid_returns_none_when_missing(self, repository: SqlAlchemyUserRepository):
        assert await repository.get_by_uid(uuid6.uuid7()) is None

    @pytest.mark.asyncio
    async def test_get_by_email(self, repository: SqlAlchemyUserRepository, user: User):
        assert await repository.get_by_email(user.email) == user

    @pytest.mark.asyncio
    async def test_get_by_email_returns_none_when_missing(self, repository: SqlAlchemyUserRepository):
        assert await repository.get_by_email(faker.email()) is None

    @pytest.mark.asyncio
    async def test_add(self, sql_test_session: AsyncSession, repository: SqlAlchemyUserRepository):
        user = UserFactory.build(
            role=UserRole.READER,
            is_active=False,
            is_superuser=False,
            is_verified=False,
        )

        assert await repository.add(user) == user
        await sql_test_session.commit()

        assert await repository.get_by_uid(user.uid) == user
