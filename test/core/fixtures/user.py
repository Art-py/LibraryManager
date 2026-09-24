import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.entities import User
from src.infrastructure.database.mappers.user import UserMapper
from test.core.factories.user import UserFactory


@pytest_asyncio.fixture()
async def user(
    request: pytest.FixtureRequest,
    sql_test_session: AsyncSession,
) -> User:
    """Создание пользователя"""
    param_value = getattr(request, 'param', {})
    user = UserFactory(
        **param_value,
    )
    sql_test_session.add(UserMapper.to_record(user))
    await sql_test_session.commit()
    return user
