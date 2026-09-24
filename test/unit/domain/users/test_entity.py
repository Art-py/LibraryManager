from uuid import UUID

from src.domain.users.entities import User
from src.domain.users.enums import UserRole


def test_user_defaults_to_reader():
    user = User(
        first_name='Ivan',
        last_name='Petrov',
        email='ivan@example.com',
        hashed_password='hashed-password',
    )

    assert isinstance(user.uid, UUID)
    assert user.role is UserRole.READER
    assert not user.is_active
    assert not user.is_superuser
    assert not user.is_verified
