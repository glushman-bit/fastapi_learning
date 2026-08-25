from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.users import (
    create_user as create_user_repository,
    delete_user as delete_user_repository,
    update_user as update_user_repository,
    get_users as get_users_repository,
    get_user_by_id,
)


def get_users(db: Session):
    """Получение списка пользователей."""
    return get_users_repository(db)


def create_user(db: Session, user_data: dict):
    """Создание пользователя."""
    try:
        return create_user_repository(db, user_data,)

    except IntegrityError:
        raise ValueError(
            "Пользователь с таким email уже существует"
        )


def get_user(db: Session, user_id: int):
    """Получение пользователя."""
    return get_user_by_id(db, user_id)


def update_user(db: Session, user_id: int, user_data: dict):
    """Изменение пользователя."""
    return update_user_repository(db, user_id, user_data)


def delete_user(db: Session, user_id: int) -> bool:
    """Удаление пользователя."""
    return delete_user_repository(db, user_id)
