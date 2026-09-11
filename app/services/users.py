from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.users import (
    create_user as create_user_repository,
    delete_user as delete_user_repository,
    update_user as update_user_repository,
    get_users as get_users_repository,
    get_user_by_id,
)
from app.exceptions import UserAlreadyExistsError


def get_users(db: Session):
    """Получение списка пользователей."""
    return get_users_repository(db)


def create_user(db: Session, user_data: dict):
    """Создание пользователя."""
    try:
        return create_user_repository(db, user_data,)

    except IntegrityError as exc:
        if (
            isinstance(exc.orig, UniqueViolation)
            and exc.orig.diag.constraint_name == "users_email_key"
        ):
            raise UserAlreadyExistsError(
                "Пользователь с таким email уже существует"
            ) from exc

        raise

    # except IntegrityError as exc:
    #     print("Ошибка БД:", exc.orig)
    #
    #     print("Тип:", type(exc.orig))
    #     print("Constraint", exc.orig.diag.constraint_name)
    #     print("Detail", exc.orig.diag.message_detail)
    #
    #     raise UserAlreadyExistsError(
    #         "Пользователь с таким email уже существует"
    #     )

    # except IntegrityError:
    #     raise UserAlreadyExistsError(
    #         "Пользователь с таким email уже существует"
    #     )


def get_user(db: Session, user_id: int):
    """Получение пользователя."""
    return get_user_by_id(db, user_id)


def update_user(db: Session, user_id: int, user_data: dict):
    """Изменение пользователя."""
    return update_user_repository(db, user_id, user_data)


def delete_user(db: Session, user_id: int) -> bool:
    """Удаление пользователя."""
    return delete_user_repository(db, user_id)
