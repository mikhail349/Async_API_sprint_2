from abc import abstractmethod, ABC
from typing import Optional, Any

from pydantic import BaseModel

from src.api.v1.query_params.base import Page


class DataStorage(ABC):
    """Абстрактный класс хранилища данных."""

    @abstractmethod
    async def get_obj(self, id: str) -> Optional[Any]:
        """Получить объект по ID.

        Args:
            id: ID объекта

        Returns:
            Optional[Any]: объект
        """
        pass

    @abstractmethod
    async def get_objects(
        self,
        page: Page,
        sort: list[str] = None,
        query: str = None,
        filter: BaseModel = None
    ) -> list[Any]:
        """Получить объекты.

        Args:
            page: пагинация
            sort: сортировка
            query: поисковый запрос
            filter: фильтрация

        Returns:
            list[Any]: список объектов

        """
        pass


class CacheStorage(ABC):
    """Абстрактный класс хранилища кеша."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Получить данные по ключу из кэша.

        Args:
            key: ключ

        Returns:
            Optional[Any]: данные
        """
        pass

    @abstractmethod
    async def put(self, key: str, value: Any):
        """Записать данные в кэш.

        Args:
            key: ключ
            value: данные
        """
        pass
