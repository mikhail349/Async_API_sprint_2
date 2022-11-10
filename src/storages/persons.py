from elasticsearch import AsyncElasticsearch

from src.api.v1.query_params.persons import Filter
from src.db.elastic import get_elastic
from src.storages.elastic import ElasticStorage


class PersonElasticStorage(ElasticStorage):
    """Класс получения персоналий из ElasticSearch.

    Args:
        es: соединение с ElasticSearch

    """
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
    """Получить инстанс класса получения персоналий из ElasticSearch.

    Returns:
        PersonElasticStorage: Класс получения персоналий из ElasticSearch

    """
    es = await get_elastic()
    return PersonElasticStorage(es=es)
