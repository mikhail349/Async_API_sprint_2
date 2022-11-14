import asyncio

import pytest
from elasticsearch import AsyncElasticsearch, helpers
from elasticsearch.exceptions import NotFoundError
from pydantic import BaseModel

from tests.functional import settings
from tests.functional.src.lib.api_client import APIClient
from tests.functional.src.lib.entity_factory import (generate_random_genre,
                                                     generate_random_person)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


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
    """Получить конструктор для добавления и удаления данных в ES."""
    def inner(index: str, data: list[BaseModel]):
        class DataHandler:

            def __init__(self, index: str, data: list[BaseModel], es_client: AsyncElasticsearch) -> None:
                self.index = index
                self.data = data
                self.es_client = es_client
            
            async def insert(self):
                query = [
                    {"_index": self.index, "_id": i.id, "_source": dict(i)}
                    for i in self.data
                ]
                _, errors = await helpers.async_bulk(self.es_client, query, refresh=True)
                if errors:
                    raise Exception("Ошибка записи в Elasticsearch")

            async def delete(self):
                try:
                    for item in self.data:
                        await self.es_client.delete(id=item.id, index=self.index)
                except NotFoundError:
                    pass

        return DataHandler(index=index, data=data, es_client=es)
    return inner


@pytest.fixture
async def api_client():
    """Объект клиента для работы с API."""
    yield APIClient()


@pytest.fixture
async def genre(es_data):
    """Создание и последующее удаление жанра в базе."""
    genre_data = generate_random_genre()
    es = es_data("genres", [genre_data])
    await es.insert()
    yield genre_data
    await es.delete()


@pytest.fixture
async def genres(es_data):
    """Создание и последующее удаление 100 жанров в базе."""
    genres_data = [generate_random_genre() for _ in range(100)]
    es = es_data("genres", genres_data)
    await es.insert()
    yield genres_data
    await es.delete()


@pytest.fixture
async def person(es_data):
    """Создание и последующее удаление персоны в базе."""
    person_data = generate_random_person()
    es = es_data("persons", [person_data])
    await es.insert()
    yield person_data
    await es.delete()


@pytest.fixture
async def persons(es_data):
    """Создание и последующее удаление 100 персон в базе."""
    persons_data = [generate_random_person() for _ in range(100)]
    es = es_data("persons", persons_data)
    await es.insert()
    yield persons_data
    await es.delete()
