import asyncpg
from sqlalchemy.exc import IntegrityError

from src.domains.core.exceptions.db_exceptions import (
    CheckConstraintException,
    DBConflictException,
    DuplicateException,
    ForeignKeyException,
    NotNullException,
)

_SQLSTATE_TO_EXCEPTION: dict[str, type[DBConflictException]] = {
    asyncpg.exceptions.UniqueViolationError.sqlstate: DuplicateException,
    asyncpg.exceptions.ForeignKeyViolationError.sqlstate: ForeignKeyException,
    asyncpg.exceptions.NotNullViolationError.sqlstate: NotNullException,
    asyncpg.exceptions.CheckViolationError.sqlstate: CheckConstraintException,
}


def map_integrity_error(error: IntegrityError) -> Exception:
    """
    Преобразует SQLAlchemy IntegrityError в доменное исключение.
    Если тип ошибки не известен — возвращает исходное IntegrityError.
    """
    orig = getattr(error, 'orig', None)
    if orig and getattr(orig, 'sqlstate', None) in _SQLSTATE_TO_EXCEPTION:
        exception_cls = _SQLSTATE_TO_EXCEPTION[orig.sqlstate]

        field_info = getattr(orig, 'constraint_name', None)
        # TODO что то придумать с сообщениями а не выдавать одно на все экспешены
        message = f'Constraint violation on {field_info}' if field_info else str(orig)

        return exception_cls(message)
    return error
