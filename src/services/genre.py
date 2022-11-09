from functools import lru_cache
from dataclasses import dataclass

from aioredis import Redis
from fastapi import Depends
from pydantic import BaseModel

from src.db.redis import get_redis
from src.models import genre
from src.services.base import BaseService
from src.storages.base import DataStorage
from src.storages.genres import get_data_storage


@dataclass
class GenreService(BaseService):
    """Сервис жанра."""
    model: BaseModel = genre.Genre
    cache_key_prefix: str = 'genres'


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        data_storage: DataStorage = Depends(get_data_storage),
) -> GenreService:
    return GenreService(redis=redis, data_storage=data_storage)
