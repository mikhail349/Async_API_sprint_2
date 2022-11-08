from abc import abstractmethod, ABC
from typing import Optional, Any

from pydantic import BaseModel

from src.api.v1.query_params.base import Page


class DataProvider(ABC):
    """Абстрактный класс для получения данных."""

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
