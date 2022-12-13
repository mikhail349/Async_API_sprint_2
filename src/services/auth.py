from http import HTTPStatus

from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
import jwt
from jwt.exceptions import InvalidTokenError

from src.core.config import jwt_settings
from src.core.messages import NO_ACCESS
from src.models.user import User

auth_scheme = HTTPBearer()
jwt_public_key = open(jwt_settings.jwt_public_key_path).read()


def raise_no_access():
    """Функция вызова Exception No access."""
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=NO_ACCESS)


def decode_jwt(token: HTTPBearer) -> dict:
    """Расшифровать JWT.
    В случае ошибки вызывает HTTPException с кодом 403.

    Args:
        token: токен

    Returns:
        dict: payload

    """
    try:
        return jwt.decode(
            token.credentials,
            jwt_public_key,
            algorithms=[jwt_settings.jwt_algorithm]
        )
    except InvalidTokenError:
        raise_no_access()


def login_required(token: HTTPBearer = Depends(auth_scheme)) -> User:
    """Dependency-функция авторизации пользователя.
    В случае ошибки вызывает HTTPException с кодом 403.

    Returns:
        User: пользователь

    """
    decoded = decode_jwt(token)
    user = User(
        username=decoded["sub"],
        is_superuser=decoded["is_superuser"],
        permissions=decoded.get("permissions")
    )
    return user


def permission_required(permission_name: str):
    """Dependency-функция проверки прав.

    Args:
        permission_name: название права

    """
    def inner(token: HTTPBearer = Depends(auth_scheme)) -> str:
        """Основная функция проверки прав.
        В случае ошибки вызывает HTTPException с кодом 403.

        Returns:
            str: username

        """
        user = login_required(token=token)

        if not user.is_superuser:
            if permission_name not in user.permissions:
                raise_no_access()
        return user
    return inner
