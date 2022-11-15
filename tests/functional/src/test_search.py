import pytest

from tests.functional.testdata import messages


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'params': {'query': 'john'}},
            {'status': 200, 'length': 2}
        ),
        (
            {'params': {'query': 'john', 'page[size]': 1}},
            {'status': 200, 'length': 1}
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
            {'status': 200, 'length': 2}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_persons(persons_search, api_client, es,
                              query_params, expected_answer):
    """Проверить поиск персоналий."""

    async def _assert():
        """Основной метод проверки персоналий."""
        data, status = await api_client.get('persons/search', **query_params['params'])
        assert status == expected_answer['status']

        if 'length' in expected_answer:
            assert len(data) == expected_answer['length']
        if 'msg' in expected_answer:
            assert data['detail'][0]['msg'] == expected_answer['msg']
    
    _assert()
    if query_params.get('test_cache'):
        for person in persons_search:
            await es.delete('persons', person.id)
        _assert()


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'params': {'query': 'show'}},
            {'status': 200, 'length': 2}
        ),
        (
            {'params': {'query': 'show', 'page[size]': 1}},
            {'status': 200, 'length': 1}
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
            {'status': 200, 'length': 2}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_genres(genres_search, api_client, es,
                             query_params, expected_answer):
    """Проверить поиск жанров."""

    async def _assert():
        """Основной метод проверки жанров."""
        data, status = await api_client.get('genres/search', **query_params['params'])
        assert status == expected_answer['status']

        if 'length' in expected_answer:
            assert len(data) == expected_answer['length']
        if 'msg' in expected_answer:
            assert data["detail"][0]["msg"] == expected_answer['msg']

    _assert()
    if query_params.get('test_cache'):
        for genre in genres_search:
            await es.delete('genres', genre.id)
        _assert()

@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'params': {'query': 'war'}},
            {'status': 200, 'length': 2}
        ),
        (
            {'params': {'query': 'war', 'page[size]': 1}},
            {'status': 200, 'length': 1}
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
            {'status': 200, 'length': 2}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_films(films_search, api_client, es,
                            query_params, expected_answer):
    """Проверить поиск фильмов."""

    async def _assert():
        """Основной метод проверки фильмов."""
        data, status = await api_client.get('films/search', **query_params['params'])
        assert status == expected_answer['status']

        if 'length' in expected_answer:
            assert len(data) == expected_answer['length']
        if 'msg' in expected_answer:
            assert data["detail"][0]["msg"] == expected_answer['msg']

    _assert()
    if query_params.get('test_cache'):
        for film in films_search:
            await es.delete('movies', film.id)
        _assert()
