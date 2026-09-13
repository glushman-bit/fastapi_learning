from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, check_user_access
from app.database import get_db
from app.models import User

from app.schemas import (UserResponse,
                         UserCreate,
                         UserUpdate,
                         LoginRequest,
                         UserUpdateFull, ChangePasswordRequest)
from app.services.users import (
    create_user as create_user_service,
    get_users as get_users_service,
    get_user as get_user_service,
    update_user as update_user_service,
    delete_user as delete_user_service, authenticate_user, change_password,
)

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user_endpoint(
        user: UserCreate,
        db: Session = Depends(get_db),
):
    """Эндпойнт: создание пользователя."""
    return create_user_service(
        db,
        user.model_dump(),  # превратит Pydantic-модель обратно в обычный Python-словарь
    )


@router.get("/users", response_model=list[UserResponse])
def get_users_endpoint(
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),   # Защита доступа от неавторизованного пользователя
):
    """Эндпойнт: получение списка пользователей."""
    return get_users_service(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(
        user_id: int,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user),
):
    """Эндпойнт: получение пользователя по id."""
    user = get_user_service(db, user_id)

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
        user_id: int,
        user: UserUpdateFull,
        db: Session = Depends(get_db),
        # user_access: User = Depends(check_user_access),    # Защита от другого пользователя
        _: User = Depends(check_user_access),   # _ - Это буквально означает: «Результат dependency мне не нужен, но саму dependency нужно выполнить».
):
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
def update_user_partial(
        user_id: int,
        user: UserUpdate,
        db: Session = Depends(get_db),
        _: User = Depends(check_user_access),
):
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
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        _: User = Depends(check_user_access),
):
    """Эндпойнт: удаление пользователя."""
    deleted_user = delete_user_service(db, user_id)

    if not deleted_user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return {"Сообщение": "Пользователь удален"}


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db),):
    """Авторизация пользователя."""
    authenticated_user = authenticate_user(
        db,
        user.email,
        user.password
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль",
        )

    token = create_access_token(authenticated_user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/users/{user_id}/change-password")
def change_password_endpoint(
        user_id: int,
        password_data: ChangePasswordRequest,
        db: Session = Depends(get_db),
        _: User = Depends(check_user_access),
):
    """Изменение пароля."""
    result = change_password(
        db,
        user_id,
        password_data.old_password,
        password_data.new_password,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Неверный старый пароль",
        )

    return {
        "message": "Пароль успешно изменен."
    }
