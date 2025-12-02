import asyncio

from db import async_session_local
from src.domains.users.enum import UserRole
from src.domains.users.model import User
from src.domains.users.security import get_hashed_password
from src.settings import get_admin_settings


async def create_user_admin():
    """
    Генерирует пользователя с администраторским доступом,
    записывает его в БД, логин и пароль берет из .env
    """

    async with async_session_local() as session:
        admin_settings = get_admin_settings()
        reg_data = {
            'first_name': 'Admin',
            'last_name': 'Admin',
            'email': admin_settings.USER_ADMIN_EMAIL,
            'hashed_password': await get_hashed_password(
                password=admin_settings.USER_ADMIN_PASSWORD.get_secret_value()
            ),
            'role': UserRole.ADMINISTRATOR,
            'is_active': True,
            'is_superuser': True,
            'is_verified': True,
        }

        user = User(**reg_data)
        session.add(user)

        try:
            await session.commit()
        except Exception:
            return 'User was created...'

        return 'User admin has been added...'


if __name__ == '__main__':
    print(asyncio.run(create_user_admin()))
