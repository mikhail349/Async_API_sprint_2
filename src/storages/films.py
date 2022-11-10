from typing import Any

from elasticsearch import AsyncElasticsearch

from src.api.v1.query_params.films import Filter
from src.db.elastic import get_elastic
from src.storages.elastic import ElasticStorage


class FilmElasticStorage(ElasticStorage):
    """Класс получения кинопроизведений из ElasticSearch.

    Args:
        es: соединение с ElasticSearch

    """
    def __init__(self, es: AsyncElasticsearch) -> None:
        super().__init__(es=es, index='movies')

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


async def get_data_storage() -> FilmElasticStorage:
    """Получить инстанс класса получения кинопроизведений из ElasticSearch.

    Returns:
        FilmElasticStorage: Класс получения кинопроизведений из ElasticSearch

    """
    es = await get_elastic()
    return FilmElasticStorage(es=es)
