from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from aioredis import Redis
from fastapi import Depends
from pydantic import BaseModel

from src.api.v1.query_params.films import Filter
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.providers.elastic import Elastic
from src.providers.base import DataProvider
from src.models.film import Film
from src.services.base import BaseService


class FilmElastic(Elastic):
    """Класс для получения кинопроизведений из ElasticSearch."""
    def compose_filters(self, filter: Filter) -> list[dict]:
        def _get_nested(field_name: str, value: Any) -> dict:
            return {
                'nested': {
                    'path': field_name,
                    'query': {
                        'match': {
                            f'{field_name}.id': value
                        }
                    }
                }
            }

        def _get(field_name: str, value: Any) -> dict:
            return {
                'term': {
                    field_name: value
                }
            }

        filters = []

        if filter.genre:
            filters.append(_get_nested('genres', filter.genre))
        if filter.actor:
            filters.append(_get_nested('actors', filter.actor))
        if filter.writer:
            filters.append(_get_nested('writers', filter.writer))
        if filter.director:
            filters.append(_get_nested('directors', filter.director))

        if filter.imdb_rating:
            filters.append(_get('imdb_rating', filter.imdb_rating))

        return filters


@dataclass
class FilmService(BaseService):
    """Сервис фильма."""
    model: BaseModel = Film
    cache_key_prefix: str = 'movies'


async def get_data_provider() -> FilmElastic:
    es = await get_elastic()
    return FilmElastic(es=es, index='movies')

@lru_cache
def get_film_service(
        redis: Redis = Depends(get_redis),
        data_provider: DataProvider = Depends(get_data_provider)
) -> FilmService:
    """Получить инстанс сервиса фильма.

    Args:
        redis: соединение с Redis
        data_provider: класс для предоставления данных

    Returns:
       FilmService: сервис фильма.

    """
    return FilmService(redis=redis, data_provider=data_provider)
