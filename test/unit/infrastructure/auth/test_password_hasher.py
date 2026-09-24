import pytest

from src.infrastructure.auth.password_hasher import BcryptPasswordHasher


@pytest.mark.asyncio
async def test_hashes_and_verifies_password():
    hasher = BcryptPasswordHasher()

    hashed_password = await hasher.hash('password123')

    assert hashed_password != 'password123'
    assert await hasher.verify('password123', hashed_password)
    assert not await hasher.verify('another-password', hashed_password)
