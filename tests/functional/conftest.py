import asyncio
import uuid

import aioredis
import pytest
from elasticsearch import AsyncElasticsearch, helpers
from faker import Faker

from tests.functional import settings
from tests.functional.src.lib import models

fake = Faker()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def es(event_loop):
    client = AsyncElasticsearch(
        hosts=[
            f"{settings.test_settings.ELASTIC_HOST}:"
            f"{settings.test_settings.ELASTIC_PORT}"
        ]
    )
    yield client
    await client.close()
    # event_loop.run_until_complete(client.close())


@pytest.fixture
async def redis_client():
    redis = await aioredis.create_redis_pool(
        (settings.test_settings.REDIS_HOST, settings.test_settings.REDIS_PORT)
    )
    yield redis
    await redis.flushall(async_op=True)
    redis.close()
    await redis.wait_closed()


@pytest.fixture
async def genre_data(es):
    return [
        models.genre.Genre(
            id=str(uuid.uuid4()), name=fake.word(), description=fake.text()
        )
    ]


@pytest.fixture
async def genre(es, genre_data):
    query = [
        {"_index": "genres", "_id": dict(g)["id"], "_source": dict(g)}
        for g in genre_data
    ]
    rows_count, errors = await helpers.async_bulk(es, query)
    if errors:
        raise Exception("Ошибка записи в Elasticsearch")
    yield genre_data[0]
    await es.close()
