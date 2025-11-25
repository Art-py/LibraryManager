from enum import StrEnum
from typing import TypeVar

T = TypeVar('T', bound='BaseEnum')


class BaseEnum(StrEnum):
    """Базовый енамчик с методом получения всех значений"""

    @classmethod
    def values(cls: type[T]) -> list[str]:
        """Получить список перечислений"""
        return [e.value for e in cls]

    @classmethod
    def has_value(cls: type[T], value: str) -> bool:
        """Проверяет, существует ли значение в перечислении"""
        return value in cls.values()
