from fastapi import Query
from pydantic import BaseModel

from src.core import config


class Page(BaseModel):
    """Модель пагинации.

    Args:
        number: номер страницы
        size: размер страницы

    """
    number: int
    size: int


def get_page(
    number: int = Query(
        default=1,
        gt=0,
        description="Номер страницы",
        alias="page[number]"
    ),
    size: int = Query(
        default=config.elastic_settings.ELASTIC_DEFAULT_PAGE_SIZE,
        gt=0,
        description="Размер страницы",
        alias="page[size]",
    )
):
    """Получить инстанс пагинации.

    Args:
        number: номер страницы
        size: размер страницы

    """
    return Page(number=number, size=size)
