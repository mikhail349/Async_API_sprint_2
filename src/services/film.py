from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from pydantic import BaseModel

from src.api.v1.query_params.films import Filter
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film
from src.services.base import BaseService


@dataclass
class FilmService(BaseService):
    """Сервис фильма.

    Args:
        redis: соединение с Redis
        elastic: соединение с Elasticsearch
        model: класс модели фильма
        es_index: название es-индекса
        es_search_fields: список полей, по которым будет осуществляться
                          полнотекстовый поиск

    """
    model: BaseModel = Film
    es_index: str = 'movies'
    es_search_fields: list[str] = field(
        default_factory=lambda: ['title', 'description']
    )

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


@lru_cache
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    """Получить инстанс сервиса фильма.

    Args:
        redis: соединение с Redis
        elastic: соединение с Elasticsearch

    Returns:
       FilmService: сервис фильма.

    """
    return FilmService(redis=redis, elastic=elastic)
