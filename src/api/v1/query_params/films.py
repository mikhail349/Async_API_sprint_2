import uuid

from pydantic import BaseModel
from fastapi import Query


class Filter(BaseModel):
    """Модель фильтрации кинопроизведения.

    Args:
        genre: ID жанра
        actor: ID актера
        writer: ID сценариста
        director: ID режиссера
        imdb_rating: Рейтинг IMDb

    """
    genre: uuid.UUID = None
    actor: uuid.UUID = None
    writer: uuid.UUID = None
    director: uuid.UUID = None
    imdb_rating: float = None


def get_filter(
    genre: uuid.UUID = Query(
        default=None,
        description='ID жанра',
        alias='filter[genre]'
    ),
    actor: uuid.UUID = Query(
        default=None,
        description='ID актера',
        alias='filter[actor]'
    ),
    writer: uuid.UUID = Query(
        default=None,
        description='ID сценариста',
        alias='filter[writer]'
    ),
    director: uuid.UUID = Query(
        default=None,
        description='ID режиссера',
        alias='filter[director]'
    ),
    imdb_rating: float = Query(
        default=None,
        ge=0,
        le=10,
        description='Рейтинг IMDb',
        alias='filter[imdb_rating]'
    )
) -> Filter:
    """Получить инстанс фильтра кинопроизведения.

    Args:
        genre: ID жанра
        actor: ID актера
        writer: ID сценариста
        director: ID режиссера
        imdb_rating: Рейтинг IMDb

    """
    return Filter(genre=genre, actor=actor, writer=writer,
                  director=director, imdb_rating=imdb_rating)
