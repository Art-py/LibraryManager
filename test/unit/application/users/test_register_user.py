from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.users.dto import RegisterUserCommand
from src.application.users.errors import PasswordMismatchError, UserAlreadyExistsError
from src.application.users.register_user import RegisterUserService
from src.domain.users.enums import UserRole


def build_dependencies():
    repository = MagicMock()
    repository.get_by_email = AsyncMock(return_value=None)
    repository.add = AsyncMock(side_effect=lambda user: user)
    unit_of_work = MagicMock(users=repository)
    unit_of_work.commit = AsyncMock()
    password_hasher = MagicMock()
    password_hasher.hash = AsyncMock(return_value='hashed-password')
    return repository, unit_of_work, password_hasher


def register_command(**overrides) -> RegisterUserCommand:
    data = {
        'first_name': 'Ivan',
        'last_name': 'Petrov',
        'second_name': None,
        'email': 'ivan@example.com',
        'password': 'password123',
        'password_confirm': 'password123',
    }
    data.update(overrides)
    return RegisterUserCommand(**data)


class TestRegisterUserService:
    @pytest.mark.asyncio
    async def test_registers_reader(self):
        repository, unit_of_work, password_hasher = build_dependencies()
        service = RegisterUserService(unit_of_work, password_hasher)

        user = await service.execute(register_command())

        assert user.email == 'ivan@example.com'
        assert user.hashed_password == 'hashed-password'
        assert user.role is UserRole.READER
        assert not user.is_active
        assert not user.is_superuser
        assert user.is_verified
        repository.add.assert_awaited_once_with(user)
        unit_of_work.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_rejects_password_mismatch(self):
        _repository, unit_of_work, password_hasher = build_dependencies()
        service = RegisterUserService(unit_of_work, password_hasher)

        with pytest.raises(PasswordMismatchError, match='Password not confirm'):
            await service.execute(register_command(password_confirm='another-password'))

        unit_of_work.commit.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_rejects_existing_email(self):
        repository, unit_of_work, password_hasher = build_dependencies()
        repository.get_by_email.return_value = object()
        service = RegisterUserService(unit_of_work, password_hasher)

        with pytest.raises(UserAlreadyExistsError, match='User is already registered'):
            await service.execute(register_command())

        unit_of_work.commit.assert_not_awaited()
