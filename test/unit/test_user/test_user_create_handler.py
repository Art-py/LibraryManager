import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.applications.users.create_user_handler import CreateUserHandler
from src.domains.users.exception import InvalidPassword, UserIsRegistered
from src.domains.users.schema import UserCreate
from src.domains.users.uow import UserUOW
from test.core.factories.user import UserFactory


@pytest_asyncio.fixture()
async def user_handler(sql_test_session: AsyncSession) -> CreateUserHandler:
    """Получение хэндлера для создания пользователя"""
    return CreateUserHandler(unit=UserUOW(session=sql_test_session))


class TestUsersHandler:
    @pytest.mark.asyncio
    async def test_user_create_success(self, user_handler: CreateUserHandler):
        user_data = UserFactory.build()

        create_data = {
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'second_name': None,
            'email': user_data.email,
            'password': '123123123',
            'password_confirm': '123123123',
        }

        created_user = await user_handler.handle(UserCreate(**create_data))

        assert created_user.uid is not None

        assert created_user.first_name == create_data['first_name']
        assert created_user.last_name == create_data['last_name']
        assert created_user.email == create_data['email']
        assert not created_user.is_active
        assert not created_user.is_superuser
        assert created_user.is_verified

    @pytest.mark.asyncio
    async def test_user_create_little_password(self, user_handler: CreateUserHandler):
        user_data = UserFactory.build()

        create_data = {
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'second_name': None,
            'email': user_data.email,
            'password': '123',
            'password_confirm': '123',
        }

        with pytest.raises(ValidationError) as _:
            await user_handler.handle(UserCreate(**create_data))

    @pytest.mark.asyncio
    async def test_user_create_not_confirm_password(self, user_handler: CreateUserHandler):
        user_data = UserFactory.build()

        create_data = {
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'second_name': None,
            'email': user_data.email,
            'password': '1234567890',
            'password_confirm': '123456789',
        }

        with pytest.raises(InvalidPassword) as _:
            await user_handler.handle(UserCreate(**create_data))

    @pytest.mark.asyncio
    async def test_user_create_failure(self, user_handler: CreateUserHandler):
        # Сначала создаем пользователя как обычно
        user_data = UserFactory.build()

        email = 'example123@example.com'

        create_data = {
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'second_name': None,
            'email': email,
            'password': '123123123',
            'password_confirm': '123123123',
        }

        created_user = await user_handler.handle(UserCreate(**create_data))

        assert created_user.uid is not None

        # Теперь пытаемся добавить пользователя с такой же почтой
        user_data = UserFactory.build()

        create_data = {
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'second_name': None,
            'email': email,
            'password': '123123123',
            'password_confirm': '123123123',
        }

        with pytest.raises(UserIsRegistered) as _:
            await user_handler.handle(UserCreate(**create_data))
