from typing import Optional

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError
import backoff

from src.core.config import elastic_settings


es: Optional[AsyncElasticsearch] = None
"""Соединение с ElasticSearch."""


async def get_elastic() -> AsyncElasticsearch:
    """Получить соединение с ElasticSearch.

    Returns:
        AsyncElasticsearch: соединение с ElasticSearch

    """
    return es


@backoff.on_exception(backoff.expo,
                      exception=ConnectionError,
                      max_time=elastic_settings.BACKOFF_MAX_TIME)
async def connect_elastic() -> AsyncElasticsearch:
    """Установить соединение с ElasticSearch.

    Returns:
        AsyncElasticsearch: соединение с ElasticSearch

    """
    global es
    es = AsyncElasticsearch(
        hosts=[f'{elastic_settings.ELASTIC_HOST}:'
               f'{elastic_settings.ELASTIC_PORT}']
    )


async def close_elastic():
    """Закрыть соединение с ElasticSearch."""
    es = await get_elastic()
    es.close()
