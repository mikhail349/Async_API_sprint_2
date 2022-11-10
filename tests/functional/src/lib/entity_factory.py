import uuid

from faker import Faker

from tests.functional.src.lib.models.genre import Genre
from tests.functional.src.lib.models.person import Person

fake = Faker()


def generate_random_genre() -> Genre:
    """Возвращает рандомный объект Genre."""
    return Genre(
        id=str(uuid.uuid4()), name=fake.word(), description=fake.text()
    )


def generate_random_person() -> Person:
    """Возвращает рандомный объект Person."""
    return Person(
        id=str(uuid.uuid4()),
        full_name=fake.name(),
        roles=["actor"],
        film_ids=[str(uuid.uuid4())],
    )
