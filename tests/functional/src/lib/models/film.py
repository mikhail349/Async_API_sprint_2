import datetime

from pydantic import BaseModel, FileUrl


class Person(BaseModel):
    """Модель персоны в фильме."""
    id: str
    name: str


class Genre(BaseModel):
    """Модель жанра в фильме."""
    id: str
    name: str


class Film(BaseModel):
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
