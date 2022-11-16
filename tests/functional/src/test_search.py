import pytest
from pydantic import BaseModel

from tests.functional.testdata import messages


class TestBaseSearch:
    """Базовый класс для теста поиска.

    Args:
        endpoint_prefix: префикс эндпоинта
        es_index: название индекса

    """
    endpoint_prefix = None
    es_index = None

    @pytest.fixture
    def assert_data(self, api_client, es):
        """Фикстура проверки данных."""
        async def inner(data: list[BaseModel],
                        query_params: dict,
                        expected_answer: dict):
            """Основной метод проверки данных.

            Args:
                data: список объектов
                query_params: словарь с входными данными
                expected_answer: словарь с ожидаемым ответом

            """
            async def _assert():
                response, status = await api_client.get(
                    f'{self.endpoint_prefix}/search',
                    **query_params['params']
                )
                assert status == expected_answer['status']

                if 'length' in expected_answer:
                    assert len(response) == expected_answer['length']
                if 'msg' in expected_answer:
                    assert (response['detail'][0]['msg']
                            == expected_answer['msg'])
                if 'ids' in expected_answer:
                    response_ids = [row['id'] for row in response]
                    assert set(response_ids) == set(expected_answer['ids'])

            await _assert()
            if query_params.get('test_cache'):
                for item in data:
                    await es.delete(self.es_index, item.id)
                await _assert()
        return inner


class TestPersonSearch(TestBaseSearch):
    """Класс для теста поиска персон."""
    endpoint_prefix = 'persons'
    es_index = 'persons'

    @pytest.mark.parametrize(
        "query_params, expected_answer",
        [
            (
                {'params': {'query': 'john'}},
                {'status': 200, 'length': 2, 'ids': ('1', '2')}
            ),
            (
                {'params': {'query': 'john', 'page[size]': 1}, 'sort': 'id'},
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
    async def test_search_persons(self, persons_search, assert_data,
                                  query_params, expected_answer):
        """Проверить поиск персоналий."""
        await assert_data(
            data=persons_search,
            query_params=query_params,
            expected_answer=expected_answer
        )


class TestGenreSearch(TestBaseSearch):
    """Класс для теста поиска жанров."""
    endpoint_prefix = 'genres'
    es_index = 'genres'

    @pytest.mark.parametrize(
        "query_params, expected_answer",
        [
            (
                {'params': {'query': 'show'}},
                {'status': 200, 'length': 2, 'ids': ('2', '3')}
            ),
            (
                {'params': {'query': 'show', 'page[size]': 1}, 'sort': 'id'},
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
    async def test_search_genres(self, genres_search, assert_data,
                                 query_params, expected_answer):
        """Проверить поиск жанров."""
        await assert_data(
            data=genres_search,
            query_params=query_params,
            expected_answer=expected_answer
        )


class TestFilmSearch(TestBaseSearch):
    """Класс для теста поиска фильмов."""
    endpoint_prefix = 'films'
    es_index = 'movies'

    @pytest.mark.parametrize(
        "query_params, expected_answer",
        [
            (
                {'params': {'query': 'war'}},
                {'status': 200, 'length': 2, 'ids': ('1', '2')}
            ),
            (
                {'params': {'query': 'war', 'page[size]': 1}, 'sort': 'id'},
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
    async def test_search_films(self, films_search, assert_data,
                                query_params, expected_answer):
        """Проверить поиск фильмов."""
        await assert_data(
            data=films_search,
            query_params=query_params,
            expected_answer=expected_answer
        )
