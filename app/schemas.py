from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Схема создания пользователя."""
    username: str = Field(min_length=3, max_length=20)
    email: str
    age: int = Field(ge=18, le=100)


class UserResponse(BaseModel):
    """Схема вывода пользователя."""
    id: int
    username: str
    email: str
    age: int
