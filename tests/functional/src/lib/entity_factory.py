import random
import uuid

from faker import Faker

from tests.functional.src.lib.models.genre import Genre
from tests.functional.src.lib.models.person import Person

fake = Faker()


def generate_random_genre(name: str = None) -> Genre:
    """Возвращает рандомный объект Genre.
    
    Args:
        name: название (по умолчанию - сгенерировать)
    
    """
    return Genre(
        id=str(uuid.uuid4()),
        name=name or fake.word(),
        description=fake.text()
    )


def generate_random_person(name: str = None) -> Person:
    """Возвращает рандомный объект Person.
    
    Args:
        name: имя (по умолчанию - сгенерировать)
    
    """
    return Person(
        id=str(uuid.uuid4()),
        full_name=name or fake.name(),
        roles=[random.choice(["actor", "writer", "director"])],
        film_ids=[str(uuid.uuid4())],
    )
