from elasticsearch import AsyncElasticsearch
from settings import test_settings

es = AsyncElasticsearch(
    hosts=[f'{test_settings.ELASTIC_HOST}:'
           f'{test_settings.ELASTIC_PORT}']
)


async def get_elastic() -> AsyncElasticsearch:
    return es
