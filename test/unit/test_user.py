import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users.enum import UserRole
from src.repositories.users.model import User
from src.repositories.users.repository import UserRepository


@pytest_asyncio.fixture()
async def repository(sql_test_session: AsyncSession) -> UserRepository:
    """Создание экземпляра UsersRepository."""
    return UserRepository(session=sql_test_session)


class TestUsers:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('user', [{'role': UserRole.READER}], indirect=True)
    async def test_get_user_by_uid(
        self,
        repository: UserRepository,
        user: User,
    ):
        user_from_bd = await repository.get_by_uid(user.uid)
        assert user_from_bd.email == user.email
