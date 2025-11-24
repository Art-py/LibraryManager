import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.applications.users.service import UserService
from src.repositories.users.schema import UserCreate
from src.repositories.users.uow import UserUOW
from test.core.factories.user import UserFactory


@pytest_asyncio.fixture()
async def user_service(sql_test_session: AsyncSession) -> UserService:
    return UserService(unit=UserUOW(session=sql_test_session))


class TestUsersService:
    @pytest.mark.asyncio
    async def test_user_create_success(self, user_service: UserService):
        user_data = UserFactory.build()

        create_data = {
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'second_name': None,
            'email': user_data.email,
            'password': '123123123',
            'password_confirm': '123123123',
        }

        created_user = await user_service.user_create(UserCreate(**create_data))

        assert created_user.uid is not None

        assert created_user.first_name == create_data['first_name']
        assert created_user.last_name == create_data['last_name']
        assert created_user.email == create_data['email']
        assert not created_user.is_active
        assert not created_user.is_superuser
        assert created_user.is_verified
