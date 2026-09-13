from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.auth import get_token, get_current_user, get_current_admin
from app.database import engine, Base, get_db
from app.exceptions import UserAlreadyExistsError, CannotDeleteSelfError
from app.models import User
from app.routers.users import router as users_router
from app.schemas import UserResponse, AdminUserResponse
from app.services.users import (
    get_users as get_users_service,
    delete_user as delete_user_service,
)



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/hello")
def hello():
    return {"message": "Hello Ivan"}


@app.get("/search")
def search(query: str | None=None):
    return {"query": query}


@app.get("/test", response_model=UserResponse)
def test():
    return {
        "username": "Ivan",
        "email": "ivan@example.com",
        "age": 21,
        "password": "secret",
        "is_admin": True,
    }


@app.exception_handler(UserAlreadyExistsError)
async def value_error_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.get("/token-test")
def token_test(token: str = Depends(get_token)):
    return {"token": token}


@app.get("/current-user")
def current_user(user: User = Depends(get_current_user)):
    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
    }


@app.get("/admin/users", response_model=list[AdminUserResponse])
def admin_get_users(
        db: Session = Depends(get_db),
        _: User = Depends(get_current_admin)
):
    return get_users_service(db)


@app.delete("/admin/users/{user_id}")
def admin_delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(get_current_admin)
):
    try:
        deleted_user = delete_user_service(
            db,
            user_id,
            admin.id,
        )

    except CannotDeleteSelfError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    if not deleted_user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return {
        "message": "Пользователь удалён",
        "deleted_user_id": user_id,
        "admin_id": admin.id,
    }

