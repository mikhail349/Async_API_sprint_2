from dataclasses import dataclass
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.api.v1.query_params.persons import Filter
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models import person
from src.services.base import BaseService


@dataclass
class PersonService(BaseService):

    def __post_init__(self):
        self.model = person.Person
        self.es_index = 'persons'
        self.es_search_fields = ['full_name']

    def compose_filters(self, filter: Filter) -> list[dict]:
        filters = []

        if filter.role:
            filters.append(
                {
                    'term': {
                        'roles': filter.role
                    }
                }
            )

        return filters


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis=redis, elastic=elastic)
