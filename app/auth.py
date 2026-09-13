import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import SECRET_KEY, JWT_ALGORITHM
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

security = HTTPBearer()


def create_access_token(user_id: int) -> str:
    """Создание access token."""
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    """Проверка и декодирование access token."""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Недействительный токен",
        )

    if "user_id" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Недействительный токен",
        )

    user_id = payload.get("user_id")

    if not isinstance(user_id, int):
        raise HTTPException(
            status_code=401,
            detail="Недействительный токен",
        )

    return payload


def get_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Получение JWT из Authorization header."""
    return credentials.credentials


def get_current_user(
        token: str = Depends(get_token),
        db: Session = Depends(get_db),
):
    """Получение user_id текущего пользователя."""
    payload = decode_token(token)

    user_id = payload["user_id"]

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Недействительный токен",
        )

    return user


def check_user_access(current_user: User, user_id: int):
    """Проверка доступа пользователя к своим данным."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Нет доступа к данным другого пользователя",
        )
