from functools import lru_cache

from aioredis import Redis
from fastapi import Depends

from src.api.v1.query_params.persons import Filter
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models import person
from src.services.base import BaseService
from src.providers.elastic import Elastic
from src.providers.base import DataProvider


class PersonElastic(Elastic):
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


async def get_data_provider() -> PersonElastic:
    es = await get_elastic()
    return PersonElastic(es=es, index='persons')


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        data_provider: DataProvider = Depends(get_data_provider),
) -> BaseService:
    return BaseService(redis=redis, data_provider=data_provider,
                       model=person.Person, cache_key_prefix='persons')
