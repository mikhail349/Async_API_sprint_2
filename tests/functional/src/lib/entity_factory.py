import random
import uuid

from faker import Faker

from tests.functional.src.lib.models.genre import Genre
from tests.functional.src.lib.models.person import Person
from tests.functional.src.lib.models.film import (Film,
                                                  Person as FilmPerson,
                                                  Genre as FilmGenre)


fake = Faker()


def generate_random_genre(id: str = None, name: str = None) -> Genre:
    """Возвращает рандомный объект Genre.

    Args:
        id: идентификатор (по умолчанию - сгенерировать)
        name: название (по умолчанию - сгенерировать)

    """
    return Genre(
        id=id or str(uuid.uuid4()),
        name=name or fake.word(),
        description=fake.text()
    )


def generate_random_person(id: str = None, name: str = None) -> Person:
    """Возвращает рандомный объект Person.

    Args:
        id: идентификатор (по умолчанию - сгенерировать)
        name: имя (по умолчанию - сгенерировать)

    """
    return Person(
        id=id or str(uuid.uuid4()),
        full_name=name or fake.name(),
        roles=[random.choice(["actor", "writer", "director"])],
        film_ids=[str(uuid.uuid4())],
    )


def generate_random_film(id: str = None, title: str = None, description: str = None) -> Film:
    """Возвращает рандомный объект Film.

    Args:
        id: идентификатор (по умолчанию - сгенерировать)
        title: название (по умолчанию - сгенерировать)
        description: описание (по умолчанию - сгенерировать)

    """
    def generate_random_filmperson() -> FilmPerson:
        """Возвращает рандомный объект FilmPerson."""
        return FilmPerson(id=str(uuid.uuid4()), name=fake.name())

    def generate_random_filmgenre() -> FilmGenre:
        """Возвращает рандомный объект FilmGenre."""
        return FilmGenre(id=str(uuid.uuid4()), name=fake.word())

    actors = [generate_random_filmperson() for _ in range(3)]
    writers = [generate_random_filmperson() for _ in range(3)]
    directors = [generate_random_filmperson() for _ in range(3)]
    genres = [generate_random_filmgenre() for _ in range(5)]

    return Film(
        id=id or str(uuid.uuid4()),
        title=title or fake.text(),
        description=description or fake.text(),
        imdb_rating=fake.random_int(0, 10),
        actors=actors,
        writers=writers,
        directors=directors,
        genres=genres
    )
