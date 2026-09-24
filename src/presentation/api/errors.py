from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.application.common.errors import PersistenceConflictError
from src.application.users.errors import (
    InvalidCredentialsError,
    PasswordMismatchError,
    TokenStorageError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

ERROR_STATUS_CODES = {
    InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
    PasswordMismatchError: status.HTTP_401_UNAUTHORIZED,
    UserAlreadyExistsError: status.HTTP_409_CONFLICT,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    TokenStorageError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    PersistenceConflictError: status.HTTP_409_CONFLICT,
}


def register_exception_handlers(app: FastAPI) -> None:
    for error_type, status_code in ERROR_STATUS_CODES.items():
        app.add_exception_handler(error_type, _handler_for(status_code))


def _handler_for(status_code: int):
    async def handle_application_error(_request: Request, error: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={'detail': str(error)})

    return handle_application_error
