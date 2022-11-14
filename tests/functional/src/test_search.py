import pytest


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'query': 'john'},
            {'length': 2}
        ),
        (
            {'query': 'bob'},
            {'length': 0}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_persons(persons_search, api_client, query_params, expected_answer):
    """Проверить поиск персоналий."""

    data, status = await api_client.get('persons/search', **query_params)
    assert status == 200
    assert len(data) == expected_answer['length']


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'query': 'action'},
            {'length': 1}
        ),
        (
            {'query': 'fake genre'},
            {'length': 0}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_genres(genres_search, api_client, query_params, expected_answer):
    """Проверить поиск жанров."""

    data, status = await api_client.get('genres/search', **query_params)
    assert status == 200
    assert len(data) == expected_answer['length']
