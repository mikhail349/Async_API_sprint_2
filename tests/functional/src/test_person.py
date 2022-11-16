import pytest

from tests.functional.testdata import default_values, messages


class TestGenre:
    """Тесты для жанров."""

    endpoint = "persons"
    index = "persons"
    list_view_fields = ["id", "full_name", "roles", "film_ids"]

    @pytest.mark.asyncio
    async def test_get_obj_by_id(self, person, api_client):
        """Проверить, что объект возвращается по запросу с корректным id."""
        data, status = await api_client.get(f"{self.endpoint}/{person.id}")
        assert status == 200
        assert data == person.dict()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("id_value", ["-1", "test"])
    async def test_wrong_id(self, person, id_value, api_client):
        """Проверить ответ на запрос с несуществующим id."""
        data, status = await api_client.get(f"{self.endpoint}/{id_value}")
        assert status == 404
        assert data == {"detail": "Персона не найдена"}

    @pytest.mark.asyncio
    async def test_list_view(self, persons, api_client):
        """Проверить получение объектов списком."""
        data, status = await api_client.get(self.endpoint)
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
    async def test_pagination(self, persons, query_params, api_client):
        """Проверить постраничный вывод объектов."""
        page_size = query_params.get("page[size]", default_values.PAGE_SIZE)
        data, status = await api_client.get(self.endpoint, **query_params)
        assert status == 200
        assert len(data) == page_size
        assert all(
            key in data[0].keys()
            for key in self.list_view_fields
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
    async def test_parameters_validation(self, person, query_params, error_msg,
                                         api_client):
        """Проверить ответы сервиса на запросы с некорректными параметрами."""
        data, status = await api_client.get(self.endpoint, **query_params)
        assert status == 422
        assert data["detail"][0]["msg"] == error_msg

    @pytest.mark.asyncio
    async def test_cache(self, person, es, api_client):
        """Проверить что данные кешируются и возвращаются сервисом после
        удаления из elastic ."""
        await api_client.get(f"{self.endpoint}/{person.id}")
        await es.delete(self.index, person.id)
        data, status = await api_client.get(f"{self.endpoint}/{person.id}")
        assert status == 200
        assert data == person.dict()

    @pytest.mark.asyncio
    async def test_filter_by_role(self, persons, api_client):
        """Проверка фильтрации по ролям."""
        data, status = await api_client.get(
            self.endpoint, **{"filter[role]": "actor"}
        )
        assert status == 200
        assert all("actor" in obj["roles"] for obj in data)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("reverse", [True, False])
    async def test_sort(self, persons, reverse, api_client):
        """Проверка сортировки."""
        perfix = "-" if reverse else ""
        data, status = await api_client.get(
            self.endpoint, **{"sort": f"{perfix}id"})
        assert status == 200
        assert [obj["id"] for obj in data] == sorted(
            [obj["id"] for obj in data], reverse=reverse)
