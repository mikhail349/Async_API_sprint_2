import pytest

from tests.functional.testdata import default_values, messages


@pytest.mark.asyncio
async def test_get_obj_by_id(person, api_client):
    """Проверить, что объект возвращается по запросу с корректным id."""
    data, status = await api_client.get(f"persons/{person.id}")
    assert status == 200
    assert data == person.dict()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_value", ["-1", "test"])
async def test_wrong_id(person, id_value, api_client):
    """Проверить ответ на запрос с несуществующим id."""
    data, status = await api_client.get(f"persons/{id_value}")
    assert status == 404
    assert data == {"detail": "Персона не найдена"}


@pytest.mark.asyncio
async def test_list_view(persons, api_client):
    """Проверить получение объектов списком."""
    data, status = await api_client.get("persons")
    assert status == 200
    assert len(data) == default_values.PAGE_SIZE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query_params",
    [
        {"page[size]": 5, "page[number]": 1},
        {"page[size]": 5},
        {"page[number]": 2},
    ],
)
async def test_pagination(persons, query_params, api_client):
    """Проверить постраничный вывод объектов."""
    page_size = query_params.get("page[size]", default_values.PAGE_SIZE)
    data, status = await api_client.get("persons", **query_params)
    assert status == 200
    assert len(data) == page_size
    assert all(
        key in data[0].keys()
        for key in ["id", "full_name", "roles", "film_ids"]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query_params, error_msg",
    [
        ({"page[size]": 0}, messages.VALUE_ZERO),
        ({"page[number]": 0}, messages.VALUE_ZERO),
        ({"page[size]": -1}, messages.VALUE_ZERO),
        ({"page[number]": -1}, messages.VALUE_ZERO),
        ({"page[size]": "test"}, messages.VALUE_NOT_INTEGER),
        ({"page[number]": "test"}, messages.VALUE_NOT_INTEGER),
    ],
)
async def test_parameters_validation(person, query_params, error_msg,
                                     api_client):
    """Проверить ответы сервиса на запросы с некорректными параметрами."""
    data, status = await api_client.get("persons", **query_params)
    assert status == 422
    assert data["detail"][0]["msg"] == error_msg


@pytest.mark.asyncio
async def test_cache(person, es, api_client):
    """Проверить что данные кешируются и возвращаются сервисом после удаления
    из elastic ."""
    await api_client.get(f"persons/{person.id}")
    await es.delete("persons", person.id)
    data, status = await api_client.get(f"persons/{person.id}")
    assert status == 200
    assert data == person.dict()


@pytest.mark.asyncio
async def test_filter_by_role(persons, api_client):
    """Проверка фильтрации по ролям."""
    data, status = await api_client.get(
        f"persons", **{"filter[role]": "actor"}
    )
    assert status == 200
    assert all("actor" in obj["roles"] for obj in data)


@pytest.mark.asyncio
@pytest.mark.parametrize("reverse", [True, False])
async def test_sort(persons, reverse, api_client):
    """Проверка сортировки."""
    perfix = "-" if reverse else ""
    data, status = await api_client.get(f"persons", **{"sort": f"{perfix}id"})
    assert status == 200
    assert [obj["id"] for obj in data] == sorted(
        [obj["id"] for obj in data], reverse=reverse
    )
