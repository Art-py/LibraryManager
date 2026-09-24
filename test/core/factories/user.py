from factory import Factory, LazyFunction
from factory.fuzzy import FuzzyChoice
from faker import Faker
from pydantic import SecretStr

from src.domain.users.entities import User
from src.domain.users.enums import UserRole
from src.infrastructure.auth.password_hasher import BcryptPasswordHasher

faker = Faker(locale='ru')


class UserFactory(Factory):
    """Фабрика пользователя"""

    first_name = LazyFunction(lambda: faker.first_name())
    last_name = LazyFunction(lambda: faker.last_name())

    email = LazyFunction(lambda: faker.email())
    hashed_password = LazyFunction(lambda: BcryptPasswordHasher.hash_sync(SecretStr(faker.password(length=10))))

    role = FuzzyChoice(list(UserRole))

    is_active = LazyFunction(lambda: faker.boolean())
    is_superuser = LazyFunction(lambda: faker.boolean())
    is_verified = LazyFunction(lambda: faker.boolean())

    class Meta:
        model = User
