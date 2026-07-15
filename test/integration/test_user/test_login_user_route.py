import pytest
from fastapi import status
from httpx import AsyncClient

from src.domains.users.model import User
from src.domains.users.security import get_hashed_password_sync

USER_URL = '/api/v1/users/login'


class TestLoginUserRoute:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user',
        [{'hashed_password': get_hashed_password_sync('user1_password123')}],
        indirect=True,
    )
    async def test_login_user_success(self, client: AsyncClient, user: User):
        data_login_user = {
            'email': user.email,
            'password': 'user1_password123',
        }
        response = await client.post(url=USER_URL, json=data_login_user)

        assert response.status_code == status.HTTP_200_OK
