import pytest
from fastapi import status
from httpx import AsyncClient

from src.repositories.users.enum import UserRole
from src.repositories.users.model import User

USER_URL = '/api/v1/users'


class TestUserRoute:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('user', [{'role': UserRole.ADMINISTRATOR}], indirect=True)
    async def test_get_user_by_uid_success(self, client: AsyncClient, user: User):
        response = await client.get(
            url=f'{USER_URL}/{user.uid}',
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        print(data)
