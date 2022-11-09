from elasticsearch import AsyncElasticsearch

from src.db.elastic import ElasticStorage, es


class GenreElasticStorage(ElasticStorage):
    """Класс для получения жанров из ElasticSearch."""
    def __init__(self, es: AsyncElasticsearch) -> None:
        super().__init__(es=es, index='genres')


async def get_data_storage() -> GenreElasticStorage:
    return GenreElasticStorage(es=es)
