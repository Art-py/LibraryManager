from sqlalchemy.exc import IntegrityError

from src.application.common.errors import PersistenceConflictError


def translate_integrity_error(error: IntegrityError) -> PersistenceConflictError:
    original_error = getattr(error, 'orig', None)
    constraint_name = getattr(original_error, 'constraint_name', None)
    message = f'Constraint violation on {constraint_name}' if constraint_name else str(original_error or error)
    return PersistenceConflictError(message)
