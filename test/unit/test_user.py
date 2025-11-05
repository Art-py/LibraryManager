import pytest
import pytest_asyncio
import uuid6
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users.enum import UserRole
from src.repositories.users.model import User
from src.repositories.users.repository import UserRepository
from test.core.utils import model_to_dict


async def assert_models_equal(obj1, obj2, exclude: set[str] = None):
    dict1 = model_to_dict(obj1, exclude)
    dict2 = model_to_dict(obj2, exclude)

    mismatches = {k: (dict1[k], dict2[k]) for k in dict1 if dict1[k] != dict2.get(k)}
    assert not mismatches, 'Objects differ:\n' + '\n'.join(f'{k}: {v1} != {v2}' for k, (v1, v2) in mismatches.items())


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
        await assert_models_equal(user, user_from_bd, exclude={'created_at', 'updated_at'})

    @pytest.mark.asyncio
    async def test_get_user_by_wrong_uid(
        self,
        repository: UserRepository,
    ):
        its_none_obj = await repository.get_by_uid(uuid6.uuid7())
        assert its_none_obj is None
