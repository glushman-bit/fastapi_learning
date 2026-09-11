from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Схема создания пользователя. Отвечает за входящие данные API."""
    username: str = Field(min_length=3, max_length=20)
    email: str
    age: int = Field(ge=18, le=100)


class UserResponse(BaseModel):
    """Схема вывода пользователя. Отвечает за исходящие данные API."""
    id: int
    username: str
    email: str
    age: int


class UserUpdate(BaseModel):
    """Схема изменения пользователя."""
    username: str | None = Field(default=None, min_length=3, max_length=20,)
    email: str | None = None
    age: int | None = Field(default=None, ge=18, le=100,)
