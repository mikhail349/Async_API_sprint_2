import pytest


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'query': 'john'},
            {'length': 2}
        ),
        (
            {'query': 'john', 'page[size]': 1},
            {'length': 1}
        ),
        (
            {'query': 'bob'},
            {'length': 0}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_persons(persons_search, api_client,
                              query_params, expected_answer):
    """Проверить поиск персоналий."""

    data, status = await api_client.get('persons/search', **query_params)
    assert status == 200
    assert len(data) == expected_answer['length']


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'query': 'show'},
            {'length': 2}
        ),
        (
            {'query': 'show', 'page[size]': 1},
            {'length': 1}
        ),
        (
            {'query': 'horror'},
            {'length': 0}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_genres(genres_search, api_client,
                             query_params, expected_answer):
    """Проверить поиск жанров."""

    data, status = await api_client.get('genres/search', **query_params)
    assert status == 200
    assert len(data) == expected_answer['length']


@pytest.mark.parametrize(
    "query_params, expected_answer",
    [
        (
            {'query': 'war'},
            {'length': 2}
        ),
        (
            {'query': 'war', 'page[size]': 1},
            {'length': 1}
        ),
        (
            {'query': 'forrest gump'},
            {'length': 0}
        ),
    ],
)
@pytest.mark.asyncio
async def test_search_films(films_search, api_client,
                            query_params, expected_answer):
    """Проверить поиск жанров."""

    data, status = await api_client.get('films/search', **query_params)
    assert status == 200
    assert len(data) == expected_answer['length']
