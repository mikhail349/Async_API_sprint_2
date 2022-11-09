from functools import lru_cache
from dataclasses import dataclass

from aioredis import Redis
from fastapi import Depends
from pydantic import BaseModel

from src.db.redis import get_redis
from src.storages.base import DataStorage
from src.models.film import Film
from src.services.base import BaseService
from src.storages.films import get_data_storage


@dataclass
class FilmService(BaseService):
    """Сервис фильма."""
    model: BaseModel = Film
    cache_key_prefix: str = 'movies'


@lru_cache
def get_film_service(
        redis: Redis = Depends(get_redis),
        data_storage: DataStorage = Depends(get_data_storage)
) -> FilmService:
    """Получить инстанс сервиса фильма.

    Args:
        redis: соединение с Redis
        data_provider: класс для предоставления данных

    Returns:
       FilmService: сервис фильма.

    """
    return FilmService(redis=redis, data_storage=data_storage)
