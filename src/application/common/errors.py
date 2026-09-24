class ApplicationError(Exception):
    """Базовая ошибка прикладного сценария."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class PersistenceConflictError(ApplicationError):
    """Ограничение хранилища не позволило сохранить изменения."""
