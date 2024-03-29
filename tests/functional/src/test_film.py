import http

import pytest

from tests.functional.src.lib.api_client import APIClient
from tests.functional.src.lib.models.film import Film
from tests.functional.src.lib.constants import default_values, messages


class TestFilm:
    """Тесты для фильмов."""

    endpoint = "films"
    index = "movies"
    list_view_fields = ['id', 'title', 'description', 'imdb_rating',
                        'creation_date']

    @pytest.mark.asyncio
    async def test_get_obj_by_id(self, film, api_client):
        """Проверить, что объект возвращается по запросу с корректным id."""
        data, status = await api_client.get(f"{self.endpoint}/{film.id}")
        assert status == http.HTTPStatus.OK
        assert Film(**data) == film

    @pytest.mark.asyncio
    @pytest.mark.parametrize("id_value", ["-1", "test"])
    async def test_wrong_id(self, film, id_value, api_client):
        """Проверить ответ на запрос с несуществующим id."""
        data, status = await APIClient().get(f"{self.endpoint}/{id_value}")
        assert status == http.HTTPStatus.NOT_FOUND
        assert data == {"detail": "Кинопроизведение не найдено"}

    @pytest.mark.asyncio
    async def test_list_view(self, films, api_client):
        """Проверить получение объектов списком."""
        data, status = await api_client.get(self.endpoint)
        assert status == http.HTTPStatus.OK
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
    async def test_pagination(self, films, query_params, api_client):
        """Проверить постраничный вывод объектов."""
        page_size = query_params.get("page[size]", default_values.PAGE_SIZE)
        data, status = await api_client.get(self.endpoint, **query_params)
        assert status == http.HTTPStatus.OK
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
    async def test_parameters_validation(self, film, query_params, error_msg,
                                         api_client):
        """Проверить ответы сервиса на запросы с некорректными параметрами."""
        data, status = await api_client.get(self.endpoint, **query_params)
        assert status == http.HTTPStatus.UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == error_msg

    @pytest.mark.asyncio
    async def test_cache(self, film, es, api_client):
        """Проверить что данные кешируются и возвращаются сервисом после
        удаления из elastic."""
        await api_client.get(f"{self.endpoint}/{film.id}")
        await es.delete(self.index, film.id)
        data, status = await api_client.get(f"{self.endpoint}/{film.id}")
        assert status == http.HTTPStatus.OK
        assert Film(**data) == film

    @pytest.mark.asyncio
    @pytest.mark.parametrize('field', ["genre", "actor", "writer", "director",
                                       "imdb_rating"])
    async def test_filter(self, films, api_client, field):
        """Проверка фильтрации."""
        value = (
            films[0].imdb_rating
            if field == "imdb_rating"
            else getattr(films[0], f"{field}s")[0].id
        )
        data, status = await api_client.get(
            self.endpoint, **{f"filter[{field}]": value})
        assert status == http.HTTPStatus.OK
        assert data[0]["id"] == films[0].id

    @pytest.mark.asyncio
    @pytest.mark.parametrize("reverse", [True, False])
    async def test_sort(self, persons, reverse, api_client):
        """Проверка сортировки."""
        perfix = "-" if reverse else ""
        data, status = await api_client.get(
            self.endpoint, **{"sort": f"{perfix}id"})
        assert status == http.HTTPStatus.OK
        assert [obj["id"] for obj in data] == sorted(
            [obj["id"] for obj in data], reverse=reverse)
