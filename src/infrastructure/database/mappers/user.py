from src.domain.users.entities import User
from src.infrastructure.database.models.user import UserRecord


class UserMapper:
    @staticmethod
    def to_domain(record: UserRecord) -> User:
        return User(
            uid=record.uid,
            first_name=record.first_name,
            last_name=record.last_name,
            second_name=record.second_name,
            email=record.email,
            hashed_password=record.hashed_password,
            role=record.role,
            is_active=record.is_active,
            is_superuser=record.is_superuser,
            is_verified=record.is_verified,
        )

    @staticmethod
    def to_record(user: User) -> UserRecord:
        return UserRecord(
            uid=user.uid,
            first_name=user.first_name,
            last_name=user.last_name,
            second_name=user.second_name,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            is_verified=user.is_verified,
        )
