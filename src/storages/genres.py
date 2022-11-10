from elasticsearch import AsyncElasticsearch

from src.db.elastic import ElasticStorage, get_elastic


class GenreElasticStorage(ElasticStorage):
    """Класс получения жанров из ElasticSearch.
    
    Args:
        es: соединение с ElasticSearch
    
    """
    def __init__(self, es: AsyncElasticsearch) -> None:
        super().__init__(es=es, index='genres')


async def get_data_storage() -> GenreElasticStorage:
    """Получить инстанс класса получения жанров из ElasticSearch.
    
    Returns:
        GenreElasticStorage: Класс получения жанров из ElasticSearch
    
    """
    es = await get_elastic()
    return GenreElasticStorage(es=es)
