import pytest
import uuid6
from fastapi import status
from httpx import AsyncClient

from src.adapters.api.v1.users.schema import UserResponse
from src.repositories.users.model import User

USER_URL = '/api/v1/users'


class TestUserRoute:
    @pytest.mark.asyncio
    async def test_get_user_by_uid_success(self, client: AsyncClient, user: User):
        response = await client.get(
            url=f'{USER_URL}/{user.uid}',
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        response_user = UserResponse(**data)

        assert response_user.uid == user.uid
        assert response_user.email == user.email
        assert response_user.first_name == user.first_name
        assert response_user.last_name == user.last_name
        assert response_user.second_name == user.second_name
        assert response_user.role == user.role
        assert response_user.is_active == user.is_active
        assert response_user.is_superuser == user.is_superuser
        assert response_user.is_verified == user.is_verified

    @pytest.mark.asyncio
    async def test_get_user_by_uid_failure(self, client: AsyncClient):
        response = await client.get(
            url=f'{USER_URL}/{uuid6.uuid7()}',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

        data = response.json()
        assert data['detail'] == 'User not found'

    @pytest.mark.asyncio
    async def test_get_user_by_wrong_uid(self, client: AsyncClient):
        response = await client.get(
            url=f'{USER_URL}/{666}',
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
