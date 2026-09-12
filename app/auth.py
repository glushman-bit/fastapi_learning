import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import SECRET_KEY, JWT_ALGORITHM

security = HTTPBearer()


def create_access_token(user_id: int) -> str:
    """Создание access token."""
    payload = {
        "user_id": user_id
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

    return payload


def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Получение JWT из Authorization header."""
    return credentials.credentials