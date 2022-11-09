from typing import Optional, Any

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel

from src.storages.base import DataStorage
from src.api.v1.query_params.base import Page


es: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    return es


class ElasticStorage(DataStorage):
    """Класс для получения данных из ElasticSearch.

    Args:
        es: соединение с ElasticSearch
        index: название индекса

    """
    def __init__(self, es: AsyncElasticsearch, index: str) -> None:
        self.es = es
        self.index = index

    def compose_filters(self, filter: BaseModel) -> list[dict]:
        """Подготовить фильтры для помещения в Query DSL:

            "query": {
                "bool": {
                    "filters": ...
                }
            }

        Args:
            filter: фильтр из параметра запроса

        Returns:
            list[dict]: список фильтров, например:
                        [
                            {
                                "term": {
                                    "field_name": "field_value"
                                }
                            }
                        ]

        """
        return []

    async def get_obj(self, id: str) -> Optional[Any]:
        try:
            doc = await self.es.get(self.index, id)
        except NotFoundError:
            return None

        return doc['_source']

    async def get_objects(
        self,
        page: Page,
        sort: list[str] = None,
        query: str = None,
        filter: BaseModel = None
    ) -> list[Any]:
        body = {}
        filters_query = []

        if filter:
            filters_query.extend(self.compose_filters(filter))

        if filters_query:
            body['query'] = {
                'bool': {
                    'filter': filters_query
                }
            }

        if sort is None:
            sort = []

        sort = [f"{x.lstrip('-')}:{'desc' if x[0] == '-' else 'asc'}"
                for x in sort]

        es_size = page.size
        es_from = (page.number - 1) * es_size

        try:
            search = await self.es.search(
                q=query,
                body=body,
                index=self.index,
                sort=sort,
                size=es_size,
                from_=es_from
            )
        except NotFoundError:
            return None

        return [doc['_source'] for doc in search['hits']['hits']]
