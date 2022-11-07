from enum import Enum

from pydantic import BaseModel
from fastapi import Query


class RolesEnum(str, Enum):
    """Перечисление ролей."""
    writer = 'writer'
    actor = 'actor'
    director = 'director'


class Filter(BaseModel):
    """Модель фильтрации персоны.

    Args:
        role: название роли

    """
    role: RolesEnum = None


def get_filter(
    role: RolesEnum = Query(
        default=None,
        description='Название роли',
        alias='filter[role]'
    )
) -> Filter:
    """Получить инстанс фильтра персоны.

    Args:
        role: название роли

    """
    return Filter(role=role)
