from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel
from elasticsearch import AsyncElasticsearch, NotFoundError

from src.api.v1.query_params.base import Page
from src.services.mixins import RedisCacheMixin


@dataclass
class BaseService(RedisCacheMixin):
    """Базовый сервис.

    Args:
        redis: соединение с Redis
        elastic: соединение с Elasticsearch
        model: класс модели фильма
        es_index: название es-индекса
        es_search_fields: список полей, по которым будет осуществляться
                          полнотекстовый поиск

    """
    elastic: AsyncElasticsearch = None
    model: BaseModel = BaseModel
    es_index: str = None
    es_search_fields: list[str] = field(default_factory=lambda: [])

    def compose_filters(self, filter: BaseModel) -> list[dict]:
        """Подготовить фильтры для помещения в Query DSL:

            "query": {
                "bool": {
                    "filters": ...
                }
            }

        Args:
            filters: список фильтров из параметров запроса

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

    def _get_objects_cache_key(
        self,
        method: str,
        page: Page,
        sort: list[str] = None,
        query: str = None,
        filter: BaseModel = None,
    ) -> str:
        """Получить ключ для списка объектов.

        Args:
            method: имя метода
            query: поисковый запрос
            filter: фильтр
            page: пагинация
            sort: сортировка

        Returns:
            str: ключ

        """
        key = (
            f'{self.es_index}/{method}'
            f'?query={query}'
            f'&page[size]={page.size}'
            f'&page[number]={page.number}'
            f'&sort={"&sort=".join(sort or [])}'
            f'&filters={filter and filter.json()}'
        )
        return key

    async def search(self,
                     query: str,
                     page: Page,
                     sort: list[str] = None) -> list[model]:
        """Найти объекты.

        Args:
            query: поисковый запрос
            page: пагинация
            sort: сортировка

        Returns:
            list[model]: список объектов

        """
        key = self._get_objects_cache_key('search',
                                          query=query,
                                          page=page,
                                          sort=sort)

        objects = await self.get_objects_from_cache(key)
        if not objects:
            objects = await self._get_objects_from_elastic(
                query=query,
                page=page,
                sort=sort
            )
            if not objects:
                return []
            await self.put_objects_to_cache(key, objects)
        return objects

    async def get(self,
                  page: Page,
                  sort: list[str] = None,
                  filter: BaseModel = None) -> list[model]:
        """Получить список объектов.

        Args:
            filter: фильтрация
            page: пагинация
            sort: сортировка

        Returns:
            list[model]: список объектов

        """
        key = self._get_objects_cache_key('get',
                                          filter=filter,
                                          page=page,
                                          sort=sort)

        objects = await self.get_objects_from_cache(key)
        if not objects:
            objects = await self._get_objects_from_elastic(
                filter=filter,
                page=page,
                sort=sort
            )
            if not objects:
                return []
            await self.put_objects_to_cache(key, objects)

        return objects

    async def get_by_id(self, obj_id: str) -> Optional[model]:
        """Получить объект по ID.

        Args:
            obj_id: ID объекта

        Returns:
            Optional[model]: объект

        """
        obj = await self.get_obj_from_cache(obj_id)
        if not obj:
            obj = await self._get_obj_from_elastic(obj_id)
            if not obj:
                return None
            await self.put_obj_to_cache(obj)

        return obj

    async def _get_obj_from_elastic(self, obj_id: str) -> Optional[model]:
        """Получить объект по ID из Elasticsearch.

        Args:
            obj_id: ID объекта

        Returns:
            Optional[model]: объект

        """
        try:
            doc = await self.elastic.get(self.es_index, obj_id)
        except NotFoundError:
            return None

        return self.model(**doc['_source'])

    async def _get_objects_from_elastic(
        self,
        page: Page,
        sort: list[str] = None,
        query: str = None,
        filter: BaseModel = None
    ) -> list[model]:
        """Получить объекты из Elasticsearch.

        Args:
            page: пагинация
            sort: сортировка
            query: поисковый запрос
            filter: фильтрация

        Returns:
            list[model]: список объектов

        """
        body = {}
        filters_query = []

        if query:
            filters_query.append(
                {
                    'multi_match': {
                        'query': query,
                        'fuzziness': 'auto',
                        'fields': self.es_search_fields
                    }
                }
            )

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
            search = await self.elastic.search(
                body=body,
                index=self.es_index,
                sort=sort,
                size=es_size,
                from_=es_from
            )
        except NotFoundError:
            return None

        return [self.model(**doc['_source']) for doc in search['hits']['hits']]
