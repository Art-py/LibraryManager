from uuid import UUID

from pydantic import BaseModel, EmailStr

from repositories.users.enum import UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    second_name: str | None

    email: EmailStr


class UserCreate(BaseModel):
    password: str
    password_confirm: str

    role: UserRole = UserRole.READER

    is_active: bool = False
    is_superuser: bool = False
    is_verified: bool = False


class UserResponse(UserBase):
    uid: UUID
