import pytest

from tests.functional.src.lib.entity_factory import generate_random_film


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
