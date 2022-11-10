import pytest

from tests.functional.src.lib.api_client import APIClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "entity, endpoint",
    [
        (pytest.lazy_fixture("genre"), "genres"),
        (pytest.lazy_fixture("person"), "persons"),
    ],
)
async def test_get_obj_by_id(entity, endpoint):
    """Проверить, что объект возвращается по запросу с корректным id."""
    data, status = await APIClient().get(f"{endpoint}/{entity.id}")
    assert status == 200
    assert data == entity.dict()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "entity, endpoint, expected_response",
    [
        (pytest.lazy_fixture("genre"), "genres", {"detail": "Жанр не найден"}),
        (
            pytest.lazy_fixture("person"),
            "persons",
            {"detail": "Персона не найдена"},
        ),
    ],
)
async def test_wrong_id(entity, endpoint, expected_response):
    """Проверить ответ на запрос с несуществующим id."""
    data, status = await APIClient().get(f"{endpoint}/-1")
    assert status == 404
    assert data == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "entity, endpoint",
    [
        (pytest.lazy_fixture("genres"), "genres"),
        (pytest.lazy_fixture("persons"), "persons"),
    ],
)
async def test_list_view(entity, endpoint):
    """Проверить получение объектов списком."""
    data, status = await APIClient().get(endpoint)
    assert status == 200
    assert len(data) == 10
