from src.models.mixin import OrjsonMixin


class Genre(OrjsonMixin):
    """Модель для жанра."""

    id: str = None
    name: str = None
    description: str = None
