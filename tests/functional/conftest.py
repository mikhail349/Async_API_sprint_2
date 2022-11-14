import asyncio

import pytest
from elasticsearch import AsyncElasticsearch, helpers
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
def es_write_data(es):
    """Фикстура для записи данных в slastic."""

    async def inner(index: str, data: list[BaseModel]):
        query = [
            {"_index": index, "_id": i.id, "_source": dict(i)}
            for i in data
        ]
        rows_count, errors = await helpers.async_bulk(es, query, refresh=True)
        if errors:
            raise Exception("Ошибка записи в Elasticsearch")

    return inner


@pytest.fixture
async def api_client():
    """Объект клиента для работы с API."""
    yield APIClient()


@pytest.fixture
async def genre(es_write_data):
    """Создание жанра в базе."""
    genre_data = generate_random_genre()
    await es_write_data("genres", [genre_data])
    yield genre_data


@pytest.fixture
async def genres(es_write_data):
    """Создание 100 жанров в базе."""
    genres_data = [generate_random_genre() for _ in range(100)]
    await es_write_data("genres", genres_data)
    yield genres_data


@pytest.fixture
async def person(es_write_data):
    """Создание персоны в базе."""
    person_data = generate_random_person()
    await es_write_data("persons", [person_data])
    yield person_data


@pytest.fixture
async def persons(es_write_data):
    """Создание 100 персон в базе."""
    persons_data = [generate_random_person() for _ in range(100)]
    await es_write_data("persons", persons_data)
    yield persons_data
