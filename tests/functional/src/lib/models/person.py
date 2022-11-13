from pydantic import BaseModel


class Person(BaseModel):
    """Модель для персоны."""

    id: str = None
    full_name: str = None
    roles: list = None
    film_ids: list = None
