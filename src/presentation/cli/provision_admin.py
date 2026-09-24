import asyncio

from src.application.users.dto import ProvisionAdminCommand
from src.application.users.errors import UserAlreadyExistsError
from src.application.users.provision_admin import ProvisionAdminService
from src.infrastructure.auth.password_hasher import BcryptPasswordHasher
from src.infrastructure.config.settings import get_admin_user_settings
from src.infrastructure.database.session import async_session_factory
from src.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork


async def provision_admin() -> str:
    settings = get_admin_user_settings()
    async with async_session_factory() as session:
        service = ProvisionAdminService(
            unit_of_work=SqlAlchemyUnitOfWork(session),
            password_hasher=BcryptPasswordHasher(),
        )
        try:
            await service.execute(
                ProvisionAdminCommand(
                    email=settings.user_admin_email,
                    password=settings.user_admin_password.get_secret_value(),
                )
            )
        except UserAlreadyExistsError:
            return 'User admin already exists.'
    return 'User admin has been added.'


if __name__ == '__main__':
    print(asyncio.run(provision_admin()))
