from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class TokenPair:
    access_token: str
    refresh_token: str


class PasswordHasher(Protocol):
    async def hash(self, password: str) -> str: ...

    async def verify(self, plain_password: str, hashed_password: str) -> bool: ...


class TokenIssuer(Protocol):
    async def issue_pair(self, user_uid: str) -> TokenPair: ...


class TokenStore(Protocol):
    async def save(self, user_uid: str, token: str) -> bool: ...

    async def get(self, user_uid: str) -> str | None: ...

    async def matches(self, user_uid: str, token: str) -> bool: ...

    async def delete(self, user_uid: str) -> bool: ...
