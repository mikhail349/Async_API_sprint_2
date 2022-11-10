import asyncio

import aioredis
import pytest
from elasticsearch import AsyncElasticsearch, helpers

from tests.functional import settings
from tests.functional.src.lib.api_client import APIClient
from tests.functional.src.lib.entity_factory import (
    generate_random_genre,
    generate_random_person,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
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
async def redis_client():
    """Клиент redis."""
    redis = await aioredis.create_redis_pool(
        (settings.test_settings.REDIS_HOST, settings.test_settings.REDIS_PORT)
    )
    yield redis
    await redis.flushall(async_op=True)
    redis.close()
    await redis.wait_closed()


@pytest.fixture
async def api_client():
    """Объект клиента для работы с API."""
    return APIClient()


@pytest.fixture
async def genre(es):
    """Создание жанра в базе."""
    genre_data = generate_random_genre()
    query = [
        {
            "_index": "genres",
            "_id": dict(genre_data)["id"],
            "_source": dict(genre_data),
        }
    ]
    rows_count, errors = await helpers.async_bulk(es, query)
    if errors:
        raise Exception("Ошибка записи в Elasticsearch")
    yield genre_data
    await es.close()


@pytest.fixture
async def genres(es):
    """Создание 100 жанров в базе."""
    genres_data = [generate_random_genre() for _ in range(100)]
    query = [
        {"_index": "genres", "_id": dict(i)["id"], "_source": dict(i)}
        for i in genres_data
    ]
    rows_count, errors = await helpers.async_bulk(es, query)
    if errors:
        raise Exception("Ошибка записи в Elasticsearch")
    yield genres_data
    await es.close()


@pytest.fixture
async def person(es):
    """Создание персоны в базе."""
    person_data = generate_random_person()
    query = [
        {
            "_index": "persons",
            "_id": dict(person_data)["id"],
            "_source": dict(person_data),
        }
    ]
    rows_count, errors = await helpers.async_bulk(es, query)
    if errors:
        raise Exception("Ошибка записи в Elasticsearch")
    yield person_data
    await es.close()


@pytest.fixture
async def persons(es):
    """Создание 100 персон в базе."""
    persons_data = [generate_random_person() for _ in range(100)]
    query = [
        {"_index": "persons", "_id": dict(i)["id"], "_source": dict(i)}
        for i in persons_data
    ]
    rows_count, errors = await helpers.async_bulk(es, query)
    if errors:
        raise Exception("Ошибка записи в Elasticsearch")
    yield persons_data
    await es.close()
