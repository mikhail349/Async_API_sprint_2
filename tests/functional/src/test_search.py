import pytest
from pydantic import BaseModel

from tests.functional.testdata import messages
from tests.functional.src.lib.api_client import APIClient
from elasticsearch import AsyncElasticsearch


async def assert_data(endpoint_prefix: str,
                      es_index: str,
                      data: list[BaseModel],
                      api_client: APIClient,
                      es_client: AsyncElasticsearch,
                      query_params: dict,
                      expected_answer: dict):
    """Основной метод проверки.
    
    Args:
        endpoint_prefix: префикс эндпоинта
        es_index: название индекса
        data: список объектов 
        api_client: клиент для выполнения API запроса
        es_client: клиент ElasticSearch
        query_params: словарь с входными данными
        expected_answer: словарь с ожидаемым ответом
    
    """
    async def _assert():
        response, status = await api_client.get(f'{endpoint_prefix}/search',
                                                **query_params['params'])
        assert status == expected_answer['status']

        if 'length' in expected_answer:
            assert len(response) == expected_answer['length']
        if 'msg' in expected_answer:
            assert response['detail'][0]['msg'] == expected_answer['msg']
        if 'ids' in expected_answer:
            response_ids = [row['id'] for row in response]
            assert set(response_ids) == set(expected_answer['ids'])

    await _assert()
    if query_params.get('test_cache'):
        for item in data:
            await es_client.delete(es_index, item.id)
        await _assert()


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'params': {'query': 'john'}},
            {'status': 200, 'length': 2, 'ids': ('1', '2')}
        ),
        (
            {'params': {'query': 'john', 'page[size]': 1}},
            {'status': 200, 'length': 1, 'ids': ('1',)}
        ),
        (
            {'params': {'query': ''}},
            {'status': 200, 'length': 0}
        ),
        (
            {'params': {}},
            {'status': 422, 'msg': messages.FIELD_REQUIRED}
        ),
        (
            {'params': {'query': 'john'}, 'test_cache': True},
            {'status': 200, 'length': 2, 'ids': ('1', '2')}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_persons(persons_search, api_client, es,
                              query_params, expected_answer):
    """Проверить поиск персоналий."""
    await assert_data(
        endpoint_prefix='persons',
        es_index='persons',
        data=persons_search,
        api_client=api_client,
        es_client=es,
        query_params=query_params,
        expected_answer=expected_answer
    )


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'params': {'query': 'show'}},
            {'status': 200, 'length': 2, 'ids': ('2', '3')}
        ),
        (
            {'params': {'query': 'show', 'page[size]': 1}},
            {'status': 200, 'length': 1, 'ids': ('2',)}
        ),
        (
            {'params': {'query': ''}},
            {'status': 200, 'length': 0}
        ),
        (
            {'params': {}},
            {'status': 422, 'msg': messages.FIELD_REQUIRED}
        ),
        (
            {'params': {'query': 'show'}, 'test_cache': True},
            {'status': 200, 'length': 2, 'ids': ('2', '3')}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_genres(genres_search, api_client, es,
                             query_params, expected_answer):
    """Проверить поиск жанров."""
    await assert_data(
        endpoint_prefix='genres',
        es_index='genres',
        data=genres_search,
        api_client=api_client,
        es_client=es,
        query_params=query_params,
        expected_answer=expected_answer
    )


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'params': {'query': 'war'}},
            {'status': 200, 'length': 2, 'ids': ('1', '2')}
        ),
        (
            {'params': {'query': 'war', 'page[size]': 1}},
            {'status': 200, 'length': 1, 'ids': ('1',)}
        ),
        (
            {'params': {'query': ''}},
            {'status': 200, 'length': 0}
        ),
        (
            {'params': {}},
            {'status': 422, 'msg': messages.FIELD_REQUIRED}
        ),
        (
            {'params': {'query': 'war'}, 'test_cache': True},
            {'status': 200, 'length': 2, 'ids': ('1', '2')}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_films(films_search, api_client, es,
                            query_params, expected_answer):
    """Проверить поиск фильмов."""
    await assert_data(
        endpoint_prefix='films',
        es_index='movies',
        data=films_search,
        api_client=api_client,
        es_client=es,
        query_params=query_params,
        expected_answer=expected_answer
    )
