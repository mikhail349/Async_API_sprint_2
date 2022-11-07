import datetime

from pydantic import FileUrl

from src.models.mixin import OrjsonMixin


class Person(OrjsonMixin):
    """Модель персоны в фильме."""
    id: str
    name: str


class Genre(OrjsonMixin):
    """Модель жанра в фильме."""
    id: str
    name: str


class Film(OrjsonMixin):
    """Модель фильма."""
    id: str
    title: str
    description: str = None
    imdb_rating: float = None
    creation_date: datetime.date = None
    file_url: FileUrl = None
    actors: list[Person] = None
    writers: list[Person] = None
    directors: list[Person] = None
    genres: list[Genre] = None
