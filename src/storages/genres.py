from elasticsearch import AsyncElasticsearch

from src.storages.elastic import ElasticStorage, get_elastic


class GenreElasticStorage(ElasticStorage):
    """Класс для получения жанров из ElasticSearch."""
    def __init__(self, es: AsyncElasticsearch) -> None:
        super().__init__(es=es, index='genres')


async def get_data_storage() -> GenreElasticStorage:
    es = await get_elastic()
    return GenreElasticStorage(es=es)
