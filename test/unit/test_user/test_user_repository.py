import pytest
import pytest_asyncio
import uuid6
from faker.proxy import Faker
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.core.exceptions.http_exceptions import NotFoundException
from src.domains.users.enum import UserRole
from src.domains.users.model import User
from src.domains.users.repository import UserRepository
from test.core.factories.user import UserFactory
from test.core.utils import model_to_dict

faker = Faker(locale='ru')


async def assert_models_equal(obj1, obj2, exclude: set[str] = None):
    dict1 = model_to_dict(obj1, exclude)
    dict2 = model_to_dict(obj2, exclude)

    mismatches = {k: (dict1[k], dict2[k]) for k in dict1 if dict1[k] != dict2.get(k)}
    assert not mismatches, 'Objects differ:\n' + '\n'.join(f'{k}: {v1} != {v2}' for k, (v1, v2) in mismatches.items())


@pytest_asyncio.fixture()
async def repository(sql_test_session: AsyncSession) -> UserRepository:
    """Создание экземпляра UsersRepository."""
    return UserRepository(session=sql_test_session)


class TestUsersRepository:
    @pytest.mark.asyncio
    async def test_get_user_by_uid(
        self,
        repository: UserRepository,
        user: User,
    ):
        result = await repository.get_by_uid(user.uid)
        assert result is not None
        await assert_models_equal(user, result, exclude={'created_at', 'updated_at'})

    @pytest.mark.asyncio
    async def test_get_user_by_wrong_uid(
        self,
        repository: UserRepository,
    ):
        with pytest.raises(NotFoundException) as exc:
            await repository.get_by_uid(uuid6.uuid7())

        assert exc.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc.value.detail == 'User not found'

    @pytest.mark.asyncio
    async def test_get_user_by_email(
        self,
        repository: UserRepository,
        user: User,
    ):
        result = await repository.get_by_email(user.email)
        assert result is not None
        await assert_models_equal(user, result, exclude={'created_at', 'updated_at'})

    @pytest.mark.asyncio
    async def test_get_user_by_wrong_email(
        self,
        repository: UserRepository,
    ):
        result = await repository.get_by_email(faker.email())
        assert result is None

    @pytest.mark.asyncio
    async def test_user_create(
        self,
        sql_test_session: AsyncSession,
        repository: UserRepository,
    ):
        user_data = UserFactory.build(
            hashed_password='9999999999',
            role=UserRole.READER,
            is_active=False,
            is_superuser=False,
            is_verified=False,
        )

        created_user = await repository.create(user_data)
        await sql_test_session.commit()

        assert created_user.uid is not None
        assert created_user.first_name == user_data.first_name
        assert created_user.last_name == user_data.last_name
        assert created_user.email == user_data.email
        assert created_user.role == UserRole.READER
        assert not created_user.is_active
        assert not created_user.is_superuser
        assert not created_user.is_verified
