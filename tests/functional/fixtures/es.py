from dataclasses import dataclass

import pytest
from elasticsearch import AsyncElasticsearch, helpers
from elasticsearch.exceptions import NotFoundError
from pydantic import BaseModel

from tests.functional import settings


@pytest.fixture(scope="session")
async def es():
    """Клиент elastic."""
    client = AsyncElasticsearch(
        hosts=[
            f"{settings.test_settings.ELASTIC_HOST}:"
            f"{settings.test_settings.ELASTIC_PORT}"
        ]
    )
    yield client
    await client.close()


@pytest.fixture
def es_data(es):
    """Фикстура для добавления и удаления данных из ES."""
    def inner(index: str, data: list[BaseModel]):
        """Получить конструктор для добавления и удаления данных из ES.

        Args:
            index: название индекса
            data: список объектов

        """
        @dataclass
        class DataHandler:
            """Класс для добавления и удаления данных из ES.

            Args:
                index: название индекса
                data: список объектов
                es_client: клиент ElasticSearch

            """
            index: str
            data: list[BaseModel]
            es_client: AsyncElasticsearch

            async def insert(self):
                """Добавить данные в ES."""
                query = [
                    {"_index": self.index, "_id": i.id, "_source": i.dict()}
                    for i in self.data
                ]
                _, errors = await helpers.async_bulk(self.es_client, query,
                                                     refresh=True)
                if errors:
                    raise Exception("Ошибка записи в Elasticsearch")

            async def delete(self):
                """Удалить данные из ES."""
                try:
                    for item in self.data:
                        await self.es_client.delete(id=item.id,
                                                    index=self.index)
                except NotFoundError:
                    pass

        return DataHandler(index=index, data=data, es_client=es)
    return inner
