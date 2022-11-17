import pytest

from tests.functional.src.lib.entity_factory import generate_random_person


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
