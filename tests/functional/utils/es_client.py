from elasticsearch import Elasticsearch

from tests.functional.settings import test_settings

es = Elasticsearch(
    hosts=[f'{test_settings.ELASTIC_HOST}:'
           f'{test_settings.ELASTIC_PORT}']
)


def get_elastic() -> Elasticsearch:
    return es
