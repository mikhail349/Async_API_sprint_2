from functools import lru_cache
from dataclasses import dataclass

from fastapi import Depends
from pydantic import BaseModel

from storages.base import get_cache_storage
from src.models import genre
from src.services.base import BaseService
from src.storages.base import DataStorage, CacheStorage
from src.storages.genres import get_data_storage


@dataclass
class GenreService(BaseService):
    """Сервис жанра."""
    model: BaseModel = genre.Genre
    cache_key_prefix: str = 'genres'


@lru_cache()
def get_genre_service(
        cache_storage: CacheStorage = Depends(get_cache_storage),
        data_storage: DataStorage = Depends(get_data_storage),
) -> GenreService:
    return GenreService(cache_storage=cache_storage,
                        data_storage=data_storage)
