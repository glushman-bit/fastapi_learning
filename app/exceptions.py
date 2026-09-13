class UserAlreadyExistsError(Exception):
    """Пользователь с таким email уже существует."""


class CannotDeleteSelfError(Exception):
    """Попытка администратора удалить самого себя."""
