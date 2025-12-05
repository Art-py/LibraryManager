import pytest
import pytest_asyncio
from fastapi import Response, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.applications.users.login_user_handler import LoginUserHandler
from src.domains.auth.token_repository import TokenRepository
from src.domains.users.exception import InvalidPassword, UserNotFound
from src.domains.users.model import User
from src.domains.users.schema import UserLogin
from src.domains.users.security import get_hashed_password_sync
from src.domains.users.uow import UserUOW


@pytest_asyncio.fixture()
async def user_handler(sql_test_session: AsyncSession, test_redis_client: Redis) -> LoginUserHandler:
    """Получение хэндлера для входа пользователя в систему"""
    return LoginUserHandler(
        unit=UserUOW(session=sql_test_session), token_repository=TokenRepository(redis_client=test_redis_client)
    )


class TestLoginUserHandler:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user',
        [{'email': 'user1@email.com', 'hashed_password': get_hashed_password_sync('123123123')}],
        indirect=True,
    )
    async def test_login_user_success(self, user: User, user_handler: LoginUserHandler):
        data_for_login = {'email': 'user1@email.com', 'password': '123123123'}
        user_login = UserLogin(**data_for_login)

        response = Response()
        result = await user_handler.handle(user_data=user_login, response=response)

        # проверяем ответ
        assert result['success']

        # проверяем что куки выставлены
        cookies = response.headers.getlist('set-cookie')

        assert any('LM_user_access_token=' in c for c in cookies)
        assert any('LM_user_refresh_token=' in c for c in cookies)

        # проверяем флаги безопасности
        for c in cookies:
            assert 'HttpOnly' in c
            assert 'Secure' in c
            assert 'SameSite=lax' in c

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user',
        [{'email': 'user2@email.com', 'hashed_password': get_hashed_password_sync('123123123')}],
        indirect=True,
    )
    async def test_login_user_wrong_email(self, user: User, user_handler: LoginUserHandler):
        data_for_login = {'email': 'user123@email.com', 'password': '123123123'}
        user_login = UserLogin(**data_for_login)

        response = Response()
        with pytest.raises(UserNotFound) as exc:
            await user_handler.handle(user_data=user_login, response=response)

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == 'Invalid credentials'

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user',
        [{'email': 'user3@email.com', 'hashed_password': get_hashed_password_sync('123123123')}],
        indirect=True,
    )
    async def test_login_user_wrong_password(self, user: User, user_handler: LoginUserHandler):
        data_for_login = {'email': 'user3@email.com', 'password': '123123123123'}
        user_login = UserLogin(**data_for_login)

        response = Response()
        with pytest.raises(InvalidPassword) as exc:
            await user_handler.handle(user_data=user_login, response=response)

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == 'Invalid credentials'
