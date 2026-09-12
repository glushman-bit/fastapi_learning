from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User


def get_users(db: Session):
    """Получение пользователей из БД."""
    statement = select(User)  # Запрос к БД == SELECT * FROM users;

    result = db.execute(statement) # Возвращает объект запроса

    return result.scalars().all()   # Вывод всех пользователей
        # scalars() говорит:
        # «Из каждой строки мне нужен первый элемент — сам объект User».
        # .all() - Забираем все найденные объекты в обычный Python-список:
        # [
        #     User(...),
        #     User(...),
        #     User(...),
        # ]


def create_user(db: Session, user_data: dict):
    """Создание пользователей в БД."""
    user = User(**user_data)

    try:
        db.add(user)  # Добавление пользователя в БД
        db.commit()   # Фиксация пользователя
        db.refresh(user)    # Обновление пользователя в БД

    except IntegrityError:
        db.rollback()    # Возврат сессии к исходному состоянию БД при ошибке
        raise

    return user


def get_user_by_id(db: Session, user_id: int):
    """Получение пользователя по id."""
    user = select(User).where(User.id==user_id)  # Создание запроса

    result = db.execute(user)   # Выполнение запроса

    return result.scalars().one_or_none()   # Вывод одного пользователя


def update_user(db: Session, user_id: int, user_data: dict,):
    """Изменение пользователя."""
    statement = select(User).where(User.id==user_id)
    result = db.execute(statement)
    user = result.scalars().one_or_none()

    if user is None:
        return None

    for field, value in user_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int) -> bool:
    """Удаление пользователя."""
    user = db.get(User, user_id)

    if user is None:
        return False

    try:
        db.delete(user)   # удаление из БД
        db.commit()

    except Exception:
        db.rollback()
        raise

    return True


# def update_user(db: Session, user_id: int, user_data: dict,):
#     """Изменение пользователя. (Универсальная функция)"""
#     user = db.get(User, user_id)
#
#     if user is None:
#         return None
#
#     for field, value in user_data.items():
#         setattr(user, field, value)
#
#     db.commit()
#     db.refresh(user)
#
#     return user
