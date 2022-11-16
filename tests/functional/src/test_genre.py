import pytest

from tests.functional.testdata import default_values, messages


class TestGenre:
    """Тесты для жанров."""

    endpoint = "genres"
    index = "genres"
    list_view_fields = ["id", "name", "description"]

    @pytest.mark.asyncio
    async def test_get_obj_by_id(self, genre, api_client):
        """Проверить, что объект возвращается по запросу с корректным id."""
        data, status = await api_client.get(f"{self.endpoint}/{genre.id}")
        assert status == 200
        assert data == genre.dict()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("id_value", ["-1", "test"])
    async def test_wrong_id(self, genre, id_value, api_client):
        """Проверить ответ на запрос с несуществующим id."""
        data, status = await api_client.get(f"{self.endpoint}/{id_value}")
        assert status == 404
        assert data == {"detail": "Жанр не найден"}

    @pytest.mark.asyncio
    async def test_list_view(self, genres, api_client):
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
            {"page[number]": 1},
        ],
    )
    async def test_pagination(self, genres, query_params, api_client):
        """Проверить постраничный вывод объектов."""
        page_size = query_params.get("page[size]", default_values.PAGE_SIZE)
        data, status = await api_client.get(self.endpoint, **query_params)
        assert status == 200
        assert len(data) == page_size
        assert all(key in data[0].keys() for key in self.list_view_fields)

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
    async def test_parameters_validation(self, genre, query_params, error_msg,
                                         api_client):
        """Проверить ответы сервиса на запросы с некорректными параметрами."""
        data, status = await api_client.get(self.endpoint, **query_params)
        assert status == 422
        assert data["detail"][0]["msg"] == error_msg

    @pytest.mark.asyncio
    async def test_cache(self, genre, es, api_client):
        """Проверить что данные кешируются и возвращаются сервисом после
        удаления из elastic."""
        await api_client.get(f"{self.endpoint}/{genre.id}")
        await es.delete(self.index, genre.id)
        data, status = await api_client.get(f"{self.endpoint}/{genre.id}")
        assert status == 200
        assert data == genre.dict()
