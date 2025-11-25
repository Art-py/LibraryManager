from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from src.domains.users.enum import UserRole
from src.domains.users.exception import PasswordNotConfirm
from src.domains.users.security import SecurityService

security_service = SecurityService()


class UserBase(BaseModel):
    first_name: str
    last_name: str
    second_name: str | None

    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=32, description='Пароль, от 8 до 32 знаков')
    password_confirm: str = Field(min_length=8, max_length=32, description='Пароль, от 8 до 32 знаков')

    @model_validator(mode='after')
    def check_password(self) -> Self:
        if self.password != self.password_confirm:
            raise PasswordNotConfirm(message='Password not confirm')
        self.password_confirm = security_service.get_hashed_password_sync(self.password)
        return self


class UserResponse(UserBase):
    uid: UUID

    role: UserRole

    is_active: bool
    is_superuser: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
