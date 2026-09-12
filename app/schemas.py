from pydantic import BaseModel, Field, ConfigDict, model_validator


class UserCreate(BaseModel):
    """Схема создания пользователя. Отвечает за входящие данные API."""
    username: str = Field(min_length=3, max_length=20)
    email: str
    age: int = Field(ge=18, le=100)
    phone: str


class UserResponse(BaseModel):
    """Схема вывода пользователя. Отвечает за исходящие данные API."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    age: int
    phone: str
    country: str




class UserUpdate(BaseModel):
    """Схема изменения пользователя."""
    username: str | None = Field(default=None, min_length=3, max_length=20,)
    email: str | None = None
    age: int | None = Field(default=None, ge=18, le=100,)

    @model_validator(mode="after")
    def reject_none_values(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} не может быть null")

        return self
