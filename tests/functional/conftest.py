import asyncio
from dataclasses import dataclass

import pytest
from elasticsearch import AsyncElasticsearch, helpers
from elasticsearch.exceptions import NotFoundError
from pydantic import BaseModel

from tests.functional import settings
from tests.functional.src.lib.api_client import APIClient
from tests.functional.src.lib.entity_factory import (generate_random_genre,
                                                     generate_random_person,
                                                     generate_random_film)


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


@pytest.fixture
async def api_client():
    """Объект клиента для работы с API."""
    yield APIClient()


@pytest.fixture
async def genre(es_data):
    """Создание жанра в базе и последующее удаление."""
    genre_data = generate_random_genre()
    es = es_data("genres", [genre_data])
    await es.insert()
    yield genre_data
    await es.delete()


@pytest.fixture
async def genres(es_data):
    """Создание 100 жанров в базе и последующее удаление."""
    genres_data = [generate_random_genre() for _ in range(100)]
    es = es_data("genres", genres_data)
    await es.insert()
    yield genres_data
    await es.delete()


@pytest.fixture
async def person(es_data):
    """Создание персоны в базе и последующее удаление."""
    person_data = generate_random_person()
    es = es_data("persons", [person_data])
    await es.insert()
    yield person_data
    await es.delete()


@pytest.fixture
async def persons(es_data):
    """Создание 100 персон в базе и последующее удаление."""
    persons_data = [generate_random_person() for _ in range(100)]
    es = es_data("persons", persons_data)
    await es.insert()
    yield persons_data
    await es.delete()


@pytest.fixture
async def film(es_data):
    """Создание фильма в базе и последующее удаление."""
    film_data = generate_random_film()
    es = es_data('movies', [film_data])
    await es.insert()
    yield film_data
    await es.delete()


@pytest.fixture
async def films(es_data):
    """Создание 100 фильмов в базе и последующее удаление."""
    films_data = [generate_random_film() for _ in range(100)]
    es = es_data('movies', films_data)
    await es.insert()
    yield films_data
    await es.delete()


@pytest.fixture
async def persons_search(es_data):
    """Создание персон в базе для поиска и последующее удаление."""

    names = ['john malkovich', 'john travolta', 'leonardo dicaprio']
    persons = [generate_random_person(id=id, name=name)
               for id, name in enumerate(names, start=1)]

    es = es_data('persons', persons)
    await es.insert()
    yield persons
    await es.delete()


@pytest.fixture
async def genres_search(es_data):
    """Создание жанров в базе для поиска и последующее удаление."""

    names = ['action', 'reality show', 'talk show']
    genres = [generate_random_genre(id=id, name=name)
              for id, name in enumerate(names, start=1)]

    es = es_data('genres', genres)
    await es.insert()
    yield genres
    await es.delete()


@pytest.fixture
async def films_search(es_data):
    """Создание фильмов в базе для поиска и последующее удаление."""

    titles = ['star wars', 'world war z', 'interstellar']
    films = [generate_random_film(id=id, title=title)
             for id, title in enumerate(titles, start=1)]

    es = es_data('movies', films)
    await es.insert()
    yield films
    await es.delete()
