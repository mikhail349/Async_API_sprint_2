from pydantic import BaseModel


class Genre(BaseModel):
    """Модель для жанра."""

    id: str = None
    name: str = None
    description: str = None
