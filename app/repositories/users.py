from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get_users(db: Session):
    """Получение пользователей из БД."""
    statement = select(User)

    result = db.execute(statement)

    return result.scalars().all()


def create_user(db: Session, user_data: dict):
    """Создание пользователей в БД."""
    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(db: Session, user_id: int):
    """Получение пользователя по id."""
    user = select(User).where(User.id==user_id)

    result = db.execute(user)

    return result.scalars().one_or_none()


def update_user(db: Session, user_id: int, user_data: dict,):
    """Изменение пользователя."""
    statement = select(User).where(User.id==user_id)
    result = db.execute(statement)
    user = result.scalars().one_or_none()

    if user is None:
        return None

    user.username = user_data["username"]
    user.email = user_data["email"]
    user.age = user_data["age"]

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int) -> bool:
    """Удаление пользователя."""
    user = db.get(User, user_id)

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True
