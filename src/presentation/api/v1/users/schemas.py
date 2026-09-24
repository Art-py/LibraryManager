from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.domain.users.enums import UserRole


class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    second_name: str | None
    email: EmailStr
    password: str = Field(min_length=8, max_length=32, description='Пароль, от 8 до 32 знаков')
    password_confirm: str = Field(min_length=8, max_length=32, description='Пароль, от 8 до 32 знаков')


class AuthenticateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32, description='Пароль, от 8 до 32 знаков')


class UserResponse(BaseModel):
    uid: UUID
    first_name: str
    last_name: str
    second_name: str | None
    email: EmailStr
    role: UserRole
    is_active: bool
    is_superuser: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class AuthenticationResponse(BaseModel):
    success: bool = True
