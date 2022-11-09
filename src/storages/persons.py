from elasticsearch import AsyncElasticsearch

from src.api.v1.query_params.persons import Filter
from src.db.elastic import ElasticStorage, get_elastic


class PersonElasticStorage(ElasticStorage):
    """Класс для получения персоналий из ElasticSearch."""

    def __init__(self, es: AsyncElasticsearch) -> None:
        super().__init__(es=es, index='persons')

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
    return PersonElasticStorage(es=es)
