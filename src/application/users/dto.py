from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterUserCommand:
    first_name: str
    last_name: str
    second_name: str | None
    email: str
    password: str
    password_confirm: str


@dataclass(frozen=True, slots=True)
class AuthenticateUserCommand:
    email: str
    password: str


@dataclass(frozen=True, slots=True)
class ProvisionAdminCommand:
    email: str
    password: str
