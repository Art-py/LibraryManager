from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from src.repositories.users.enum import UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    second_name: str | None

    email: EmailStr


class UserCreate(UserBase):
    password: str
    password_confirm: str


class UserResponse(UserBase):
    uid: UUID

    role: UserRole

    is_active: bool
    is_superuser: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
