from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.users.dto import ProvisionAdminCommand
from src.application.users.provision_admin import ProvisionAdminService
from src.domain.users.enums import UserRole


@pytest.mark.asyncio
async def test_provisions_active_administrator():
    repository = MagicMock()
    repository.get_by_email = AsyncMock(return_value=None)
    repository.add = AsyncMock(side_effect=lambda user: user)
    unit_of_work = MagicMock(users=repository)
    unit_of_work.commit = AsyncMock()
    password_hasher = MagicMock()
    password_hasher.hash = AsyncMock(return_value='hashed-password')
    service = ProvisionAdminService(unit_of_work, password_hasher)

    user = await service.execute(ProvisionAdminCommand('admin@example.com', 'password123'))

    assert user.role is UserRole.ADMINISTRATOR
    assert user.is_active
    assert user.is_superuser
    assert user.is_verified
    unit_of_work.commit.assert_awaited_once()
