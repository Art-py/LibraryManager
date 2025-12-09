import pytest
from fastapi import status
from httpx import AsyncClient

from src.domains.users.enum import UserRole
from src.domains.users.model import User

USER_URL = '/api/v1/users/register'


class TestRegisterUserRoute:
    @pytest.mark.asyncio
    async def test_register_user_success(self, client: AsyncClient):
        data_register_user = {
            'first_name': 'Ivan',
            'last_name': 'Meleshenko',
            'second_name': 'Aleksandrovich',
            'email': 'Test@example.com',
            'password': '123123123',
            'password_confirm': '123123123',
        }
        response = await client.post(url=USER_URL, json=data_register_user)

        assert response.status_code == status.HTTP_200_OK

        registered_user = response.json()

        assert registered_user.get('uid') is not None
        assert registered_user.get('first_name') == data_register_user.get('first_name')
        assert registered_user.get('last_name') == data_register_user.get('last_name')
        assert registered_user.get('second_name') == data_register_user.get('second_name')
        assert registered_user.get('email') == data_register_user.get('email')
        assert registered_user.get('role') == UserRole.READER
        assert not registered_user.get('is_active')
        assert not registered_user.get('is_superuser')
        assert registered_user.get('is_verified')

    @pytest.mark.asyncio
    async def test_register_user_password_not_confirm(self, client: AsyncClient):
        data_register_user = {
            'first_name': 'Ivan',
            'last_name': 'Meleshenko',
            'second_name': 'Aleksandrovich',
            'email': 'Test@example.com',
            'password': '1231231233333',
            'password_confirm': '123123123',
        }
        response = await client.post(url=USER_URL, json=data_register_user)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        data = response.json()
        assert data['detail'] == 'Password not confirm'

    @pytest.mark.asyncio
    async def test_register_user_registered(self, client: AsyncClient, user: User):
        data_register_user = {
            'first_name': 'Ivan',
            'last_name': 'Meleshenko',
            'second_name': 'Aleksandrovich',
            'email': user.email,
            'password': '123123123',
            'password_confirm': '123123123',
        }
        response = await client.post(url=USER_URL, json=data_register_user)

        assert response.status_code == status.HTTP_409_CONFLICT

        data = response.json()
        assert data['detail'] == 'User is already registered'
