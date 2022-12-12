from http import HTTPStatus

from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
import jwt
from jwt.exceptions import InvalidTokenError

from src.core.config import jwt_settings

auth_scheme = HTTPBearer()
jwt_public_key = open(jwt_settings.jwt_public_key_path).read()


def raise_no_access():
    """Функция вызова Exception No access."""
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="No access")


def decode_jwt(token: str) -> dict:
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


def login_required(token: str = Depends(auth_scheme)) -> str:
    """Dependency-функция авторизации пользователя.
    В случае ошибки вызывает HTTPException с кодом 403.

    Returns:
        str: username

    """
    decoded = decode_jwt(token)
    return decoded.get('sub')


def permission_required(permission_name: str):
    """Dependency-функция проверки прав.

    Args:
        permission_name: название права

    """
    def inner(token: str = Depends(auth_scheme)) -> str:
        """Основная функция проверки прав.
        В случае ошибки вызывает HTTPException с кодом 403.

        Returns:
            str: username

        """
        decoded = decode_jwt(token)
        username = decoded.get('sub')
        if decoded.get('is_superuser'):
            return username
        if permission_name not in decoded.get('permissions'):
            raise_no_access()
        return username
    return inner
