from src.models.mixin import OrjsonMixin


class User(OrjsonMixin):
    """Модель для пользователя."""

    username: str
    is_superuser: bool
    permissions: list[str]
