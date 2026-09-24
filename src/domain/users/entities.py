from dataclasses import dataclass, field
from uuid import UUID

import uuid6

from src.domain.users.enums import UserRole


@dataclass(slots=True, kw_only=True)
class User:
    """Пользователь библиотеки."""

    first_name: str
    last_name: str
    email: str
    hashed_password: str
    second_name: str | None = None
    role: UserRole = UserRole.READER
    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False
    uid: UUID = field(default_factory=uuid6.uuid7)
