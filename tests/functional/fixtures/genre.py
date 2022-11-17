import pytest

from tests.functional.src.lib.entity_factory import generate_random_genre


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
async def genres_search(es_data):
    """Создание жанров в базе для поиска и последующее удаление."""

    names = ['action', 'reality show', 'talk show']
    genres = [generate_random_genre(id=id, name=name)
              for id, name in enumerate(names, start=1)]

    es = es_data('genres', genres)
    await es.insert()
    yield genres
    await es.delete()
