from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.common.auth import TokenPair
from src.application.users.authenticate_user import AuthenticateUserService
from src.application.users.dto import AuthenticateUserCommand
from src.application.users.errors import InvalidCredentialsError, TokenStorageError
from src.domain.users.entities import User


def build_service(user: User | None, password_matches: bool = True, token_saved: bool = True):
    repository = MagicMock()
    repository.get_by_email = AsyncMock(return_value=user)
    unit_of_work = MagicMock(users=repository)
    password_hasher = MagicMock()
    password_hasher.verify = AsyncMock(return_value=password_matches)
    token_issuer = MagicMock()
    token_issuer.issue_pair = AsyncMock(return_value=TokenPair('access-token', 'refresh-token'))
    token_store = MagicMock()
    token_store.save = AsyncMock(return_value=token_saved)
    service = AuthenticateUserService(unit_of_work, password_hasher, token_issuer, token_store)
    return service, password_hasher, token_issuer, token_store


class TestAuthenticateUserService:
    @pytest.mark.asyncio
    async def test_issues_and_stores_tokens(self):
        user = User(
            first_name='Ivan',
            last_name='Petrov',
            email='ivan@example.com',
            hashed_password='hashed-password',
        )
        service, password_hasher, token_issuer, token_store = build_service(user)

        tokens = await service.execute(AuthenticateUserCommand(user.email, 'password123'))

        assert tokens == TokenPair('access-token', 'refresh-token')
        password_hasher.verify.assert_awaited_once_with('password123', 'hashed-password')
        token_issuer.issue_pair.assert_awaited_once_with(str(user.uid))
        token_store.save.assert_awaited_once_with(str(user.uid), 'access-token')

    @pytest.mark.asyncio
    @pytest.mark.parametrize(('user_exists', 'password_matches'), [(False, True), (True, False)])
    async def test_rejects_invalid_credentials(self, user_exists, password_matches):
        user = (
            User(
                first_name='Ivan',
                last_name='Petrov',
                email='ivan@example.com',
                hashed_password='hashed-password',
            )
            if user_exists
            else None
        )
        service, _password_hasher, token_issuer, _token_store = build_service(user, password_matches)

        with pytest.raises(InvalidCredentialsError, match='Invalid credentials'):
            await service.execute(AuthenticateUserCommand('unknown@example.com', 'password123'))

        token_issuer.issue_pair.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_fails_when_access_token_cannot_be_stored(self):
        user = User(
            first_name='Ivan',
            last_name='Petrov',
            email='ivan@example.com',
            hashed_password='hashed-password',
        )
        service, _password_hasher, _token_issuer, _token_store = build_service(user, token_saved=False)

        with pytest.raises(TokenStorageError, match='Token storage failed'):
            await service.execute(AuthenticateUserCommand(user.email, 'password123'))
