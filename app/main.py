from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from app.auth import get_token, get_current_user, get_current_admin
from app.database import engine, Base
from app.exceptions import UserAlreadyExistsError
from app.models import User
from app.routers.users import router as users_router
from app.schemas import UserResponse


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


@app.get("/admin-test")
def admin_test(admin: User = Depends(get_current_admin)):
    return {
        "message": "Доступ разрешен",
        "user_id": admin.id,
        "username": admin.is_admin,
    }
