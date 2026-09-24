from src.domain.users.entities import User
from src.domain.users.enums import UserRole
from src.infrastructure.database.mappers.user import UserMapper


def test_maps_user_to_record_and_back():
    user = User(
        first_name='Ivan',
        last_name='Petrov',
        second_name='Ivanovich',
        email='ivan@example.com',
        hashed_password='hashed-password',
        role=UserRole.LIBRARIAN,
        is_active=True,
        is_verified=True,
    )

    restored_user = UserMapper.to_domain(UserMapper.to_record(user))

    assert restored_user == user
