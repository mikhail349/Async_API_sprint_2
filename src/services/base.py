from dataclasses import dataclass
from typing import Optional, Any

from pydantic import BaseModel

from src.api.v1.query_params.base import Page
from src.services.mixins import RedisCacheMixin
from src.providers.base import DataProvider


@dataclass
class BaseService(RedisCacheMixin):
    """Базовый сервис.

    Args:
        model: класс модели
        data_provider: поставщик данных
        cache_key_prefix: префикс для ключа кэша

    """
    model: BaseModel = None
    data_provider: DataProvider = None
    cache_key_prefix: str = None

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
            f'{self.cache_key_prefix}/{method}'
            f'?query={query}'
            f'&page[size]={page.size}'
            f'&page[number]={page.number}'
            f'&sort={"&sort=".join(sort or [])}'
            f'&filters={filter and filter.json()}'
        )
        return key

    def _transform_objects_from_data(self, objects: list) -> list[model]:
        """Трансформировать входящие объекты.

        Args:
            objects: объекты

        Returns:
            list[model]: объекты класса model

        """
        if not objects:
            return []
        return [self.model(**obj) for obj in objects]

    def _transform_obj_from_data(self, obj: Optional[Any]) -> Optional[model]:
        """Трансформировать входящий объект.

        Args:
            obj: объект

        Returns:
            Optional[model]: объект класса model

        """
        if not obj:
            return None
        return self.model(**obj)

    def _transform_objects_from_cache(self,
                                      objects: Optional[Any]) -> list[model]:
        """Трансформировать объекты из кэша.

        Args:
            objects: объекты

        Returns:
            list[model]: объекты класса model

        """
        if not objects:
            return []
        json_loads = self.model.Config.json_loads
        objects = json_loads(objects)
        return [self.model.parse_obj(obj) for obj in objects]

    def _transform_obj_from_cache(self, obj: Optional[Any]) -> Optional[model]:
        """Трансформировать объект из кэша.

        Args:
            obj: объект

        Returns:
            list[model]: объект класса model

        """
        if not obj:
            return None
        return self.model.parse_raw(obj)

    def _transform_objects_to_cache(self, objects: list[model]) -> str:
        """Трансформировать объекты в кэш.

        Args:
            objects: объекты

        Returns:
            str: json

        """
        json_dumps = self.model.Config.json_dumps
        return json_dumps([obj.dict() for obj in objects], default=str)

    def _transform_obj_to_cache(self, obj: model) -> str:
        """Трансформировать объект в кэш.

        Args:
            obj: объект

        Returns:
            str: json

        """
        return obj.json()

    async def _get_objects(
        self,
        method: str,
        page: Page,
        query: str = None,
        sort: list[str] = None,
        filter: BaseModel = None
    ) -> list[model]:
        """Получить список объектов с учетом поиска и фильтрации.

        Args:
            method: название метода для ключа кэша
            query: поисковый запрос
            page: пагинация
            sort: сортировка
            filter: фильтрация

        Returns:
            list[model]: список объектов

        """
        key = self._get_objects_cache_key(method=method,
                                          query=query,
                                          page=page,
                                          sort=sort,
                                          filter=filter)

        objects = await self.get_obj_from_cache(key)
        # TODO: objects = await self.cache_provider.get(key)
        objects = self._transform_objects_from_cache(objects)

        if not objects:
            objects = await self.data_provider.get_objects(
                query=query,
                page=page,
                sort=sort,
                filter=filter
            )
            objects = self._transform_objects_from_data(objects)
            if not objects:
                return []

            cache = self._transform_objects_to_cache(objects)
            await self.put_obj_to_cache(key, cache)
            # TODO: await self.cache_provider.put(key, cache)

        return objects

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
        return await self._get_objects(method='search',
                                       page=page, query=query, sort=sort)

    async def get(self,
                  page: Page,
                  sort: list[str] = None,
                  filter: BaseModel = None) -> list[model]:
        """Получить список объектов.

        Args:
            page: пагинация
            sort: сортировка
            filter: фильтрация

        Returns:
            list[model]: список объектов

        """
        return await self._get_objects(method='get',
                                       page=page, sort=sort, filter=filter)

    async def get_by_id(self, obj_id: str) -> Optional[model]:
        """Получить объект по ID.

        Args:
            obj_id: ID объекта

        Returns:
            Optional[model]: объект

        """
        obj = await self.get_obj_from_cache(obj_id)
        # TODO: obj = await self.cache_provider.get(obj_id)
        obj = self._transform_obj_from_cache(obj)

        if not obj:
            obj = await self.data_provider.get_obj(obj_id)
            obj = self._transform_obj_from_data(obj)
            if not obj:
                return None

            cache = self._transform_obj_to_cache(obj)
            await self.put_obj_to_cache(obj.id, cache)
            # TODO: await self.cache_provider.put(obj.id, cache)

        return obj
