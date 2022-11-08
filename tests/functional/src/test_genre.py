import pytest

from tests.functional.src.lib.api_client import APIClient
from tests.functional.src.lib.models.genre import Genre


@pytest.mark.asyncio
async def test_get_genre_by_id(genre):
    data, status = await APIClient().get_by_id(genre.id)
    assert status == 200
    assert Genre(**data) == genre
