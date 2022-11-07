from dataclasses import dataclass
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models import genre
from src.services.base import BaseService


@dataclass
class GenreService(BaseService):

    def __post_init__(self):
        self.model = genre.Genre
        self.es_index = 'genres'
        self.es_search_fields = ['name', 'description']


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis=redis, elastic=elastic)
