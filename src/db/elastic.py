from typing import Optional

from elasticsearch import AsyncElasticsearch


es: Optional[AsyncElasticsearch] = None
"""Соединение с ElasticSearch."""


async def get_elastic() -> AsyncElasticsearch:
    """Получить соединение с ElasticSearch.
    
    Returns:
        AsyncElasticsearch: соединение с ElasticSearch
    
    """
    return es
