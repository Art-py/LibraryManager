from fastapi import status

from src.repositories.core.base_exception import BaseException


class DBConflictException(BaseException):
    """Базовый класс для эксепшенов при работе с БД"""

    def __init__(self, message: str, code: int = status.HTTP_409_CONFLICT):
        super().__init__(code=code, message=f'{self.__class__.__name__}: {message}')


class DuplicateException(DBConflictException):
    """Нарушено уникальное ограничение"""

    pass


class ForeignKeyException(DBConflictException):
    """Нарушено ограничение внешнего ключа"""

    pass


class NotNullException(DBConflictException):
    """Нарушено ограничение NOT NULL"""

    pass


class CheckConstraintException(DBConflictException):
    """Нарушено ограничение CHECK"""

    pass
