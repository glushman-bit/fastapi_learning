from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas import UserResponse, UserCreate, UserUpdate
from app.services.users import (
    create_user as create_user_service,
    get_users as get_users_service,
    get_user as get_user_service,
    update_user as update_user_service,
    delete_user as delete_user_service,
)

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db),):
    """Эндпойнт: создание пользователя."""
    return create_user_service(
        db,
        user.model_dump(),  # превратит Pydantic-модель обратно в обычный Python-словарь
    )


@router.get("/users")
def get_users_endpoint(db: Session = Depends(get_db),):
    """Эндпойнт: получение списка пользователей."""
    return get_users_service(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db),):
    """Эндпойнт: получение пользователя по id."""
    user = get_user_service(db, user_id)

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db),):
    """Эндпойнт: изменение пользователя."""
    updated_user = update_user_service(
        db,
        user_id,
        user.model_dump(),
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return updated_user


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user_partial(user_id: int, user: UserUpdate, db: Session = Depends(get_db),):
    """Эндпойнт: Частичное изменение пользователя."""
    updated_user = update_user_service(
        db,
        user_id,
        user.model_dump(exclude_unset=True),
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )

    return updated_user


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db),):
    """Эндпойнт: удаление пользователя."""
    deleted_user = delete_user_service(db, user_id)

    if not deleted_user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return {"Сообщение": "Пользователь удален"}
