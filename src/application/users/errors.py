from src.application.common.errors import ApplicationError


class InvalidCredentialsError(ApplicationError):
    pass


class PasswordMismatchError(ApplicationError):
    pass


class UserAlreadyExistsError(ApplicationError):
    pass


class UserNotFoundError(ApplicationError):
    pass


class TokenStorageError(ApplicationError):
    pass
