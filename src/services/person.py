from functools import lru_cache
from dataclasses import dataclass

from aioredis import Redis
from fastapi import Depends
from pydantic import BaseModel

from src.api.v1.query_params.persons import Filter
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models import person
from src.services.base import BaseService
from src.storages.elastic import ElasticStorage
from src.storages.base import DataStorage


class PersonElasticStorage(ElasticStorage):
    """Класс для получения персоналий из ElasticSearch."""
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


async def get_data_storage() -> PersonElasticStorage:
    es = await get_elastic()
    return PersonElasticStorage(es=es, index='persons')


@dataclass
class PersonService(BaseService):
    """Сервис персоны."""
    model: BaseModel = person.Person
    cache_key_prefix: str = 'persons'


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        data_storage: DataStorage = Depends(get_data_storage),
) -> PersonService:
    return PersonService(redis=redis, data_storage=data_storage)
