from fastapi import FastAPI

from app.database import engine, Base
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
