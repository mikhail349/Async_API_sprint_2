from functools import lru_cache
from dataclasses import dataclass

from fastapi import Depends
from pydantic import BaseModel

from src.storages.redis import get_redis_storage, RedisStorage
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
        redis_storage: RedisStorage = Depends(get_redis_storage),
        data_storage: DataStorage = Depends(get_data_storage),
) -> GenreService:
    return GenreService(redis_storage=redis_storage,
                        data_storage=data_storage)
