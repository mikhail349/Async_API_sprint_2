from dataclasses import dataclass
from functools import lru_cache

from aioredis import Redis
from fastapi import Depends
from pydantic import BaseModel

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models import genre
from src.services.base import BaseService
from src.providers.base import DataProvider
from src.providers.elastic import Elastic


@dataclass
class GenreService(BaseService):
    """Сервис жанра."""
    model: BaseModel = genre.Genre
    cache_key_prefix: str = 'genres'


async def get_data_provider() -> Elastic:
    es = await get_elastic()
    return Elastic(es=es, index='genres')

@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        data_provider: DataProvider = Depends(get_data_provider),
) -> GenreService:
    return GenreService(redis=redis, data_provider=data_provider)
