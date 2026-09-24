import pytest
import uuid6
from fastapi import status
from httpx import AsyncClient

from src.domain.users.entities import User
from src.domain.users.enums import UserRole
from src.infrastructure.auth.password_hasher import BcryptPasswordHasher
from src.presentation.api.v1.users.schemas import UserResponse

REGISTER_URL = '/api/v1/users/register'
LOGIN_URL = '/api/v1/users/login'
USERS_URL = '/api/v1/users'


def registration_data(**overrides) -> dict:
    data = {
        'first_name': 'Ivan',
        'last_name': 'Meleshenko',
        'second_name': 'Aleksandrovich',
        'email': 'test@example.com',
        'password': '123123123',
        'password_confirm': '123123123',
    }
    data.update(overrides)
    return data


class TestRegisterUserRoute:
    @pytest.mark.asyncio
    async def test_register_user_success(self, client: AsyncClient):
        request_data = registration_data()

        response = await client.post(REGISTER_URL, json=request_data)

        assert response.status_code == status.HTTP_200_OK
        registered_user = UserResponse(**response.json())
        assert registered_user.first_name == request_data['first_name']
        assert registered_user.last_name == request_data['last_name']
        assert registered_user.email == request_data['email']
        assert registered_user.role is UserRole.READER
        assert not registered_user.is_active
        assert not registered_user.is_superuser
        assert registered_user.is_verified

    @pytest.mark.asyncio
    async def test_rejects_password_mismatch(self, client: AsyncClient):
        response = await client.post(
            REGISTER_URL,
            json=registration_data(password_confirm='different-password'),
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['detail'] == 'Password not confirm'

    @pytest.mark.asyncio
    async def test_rejects_short_password(self, client: AsyncClient):
        response = await client.post(
            REGISTER_URL,
            json=registration_data(password='short', password_confirm='short'),
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    @pytest.mark.asyncio
    async def test_rejects_registered_email(self, client: AsyncClient, user: User):
        response = await client.post(REGISTER_URL, json=registration_data(email=user.email))

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()['detail'] == 'User is already registered'


class TestAuthenticateUserRoute:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user',
        [{'hashed_password': BcryptPasswordHasher.hash_sync('user1_password123')}],
        indirect=True,
    )
    async def test_login_sets_secure_cookies(self, client: AsyncClient, user: User):
        response = await client.post(
            LOGIN_URL,
            json={'email': user.email, 'password': 'user1_password123'},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'success': True}
        cookies = response.headers.get_list('set-cookie')
        assert any('LM_user_access_token=' in cookie for cookie in cookies)
        assert any('LM_user_refresh_token=' in cookie for cookie in cookies)
        assert all('HttpOnly' in cookie and 'Secure' in cookie and 'SameSite=lax' in cookie for cookie in cookies)

    @pytest.mark.asyncio
    async def test_rejects_unknown_user(self, client: AsyncClient):
        response = await client.post(
            LOGIN_URL,
            json={'email': 'unknown@example.com', 'password': 'password123'},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['detail'] == 'Invalid credentials'


class TestGetUserRoute:
    @pytest.mark.asyncio
    async def test_get_user_by_uid(self, client: AsyncClient, user: User):
        response = await client.get(f'{USERS_URL}/{user.uid}')

        assert response.status_code == status.HTTP_200_OK
        assert UserResponse(**response.json()).uid == user.uid

    @pytest.mark.asyncio
    async def test_get_missing_user(self, client: AsyncClient):
        response = await client.get(f'{USERS_URL}/{uuid6.uuid7()}')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()['detail'] == 'User not found'

    @pytest.mark.asyncio
    async def test_rejects_invalid_uid(self, client: AsyncClient):
        response = await client.get(f'{USERS_URL}/666')

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
