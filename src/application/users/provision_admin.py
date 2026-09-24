from src.application.common.auth import PasswordHasher
from src.application.common.unit_of_work import UnitOfWork
from src.application.users.dto import ProvisionAdminCommand
from src.application.users.errors import UserAlreadyExistsError
from src.domain.users.entities import User
from src.domain.users.enums import UserRole


class ProvisionAdminService:
    """Создаёт первоначальную административную учётную запись."""

    def __init__(self, unit_of_work: UnitOfWork, password_hasher: PasswordHasher):
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher

    async def execute(self, command: ProvisionAdminCommand) -> User:
        if await self._unit_of_work.users.get_by_email(command.email) is not None:
            raise UserAlreadyExistsError('User is already registered')

        user = User(
            first_name='Admin',
            last_name='Admin',
            email=command.email,
            hashed_password=await self._password_hasher.hash(command.password),
            role=UserRole.ADMINISTRATOR,
            is_active=True,
            is_superuser=True,
            is_verified=True,
        )
        created_user = await self._unit_of_work.users.add(user)
        await self._unit_of_work.commit()
        return created_user
