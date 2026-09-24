from unittest.mock import AsyncMock, MagicMock

import pytest
import uuid6

from src.application.users.errors import UserNotFoundError
from src.application.users.get_user import GetUserService
from src.domain.users.entities import User


class TestGetUserService:
    @pytest.mark.asyncio
    async def test_returns_user(self):
        user = User(
            first_name='Ivan',
            last_name='Petrov',
            email='ivan@example.com',
            hashed_password='hashed-password',
        )
        repository = MagicMock()
        repository.get_by_uid = AsyncMock(return_value=user)
        service = GetUserService(MagicMock(users=repository))

        assert await service.execute(user.uid) == user

    @pytest.mark.asyncio
    async def test_raises_when_user_is_missing(self):
        repository = MagicMock()
        repository.get_by_uid = AsyncMock(return_value=None)
        service = GetUserService(MagicMock(users=repository))

        with pytest.raises(UserNotFoundError, match='User not found'):
            await service.execute(uuid6.uuid7())
