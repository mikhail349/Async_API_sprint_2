from src.models.mixin import OrjsonMixin


class Person(OrjsonMixin):
    """Модель для персоны."""

    id: str = None
    full_name: str = None
    roles: list = None
    film_ids: list = None
