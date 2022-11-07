from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Path

from src.api.v1.query_params.base import Page, get_page
from src.api.v1.query_params.films import Filter, get_filter
from src.api.v1.models.film import FilmList, FilmDetails
from src.services.film import FilmService, get_film_service
from src.core.messages import messages

router = APIRouter()


@router.get('/search',
            response_model=list[FilmList],
            summary='Поиск кинопроизведений',
            description='Полнотекстовый поиск кинопроизведений '
                        'с пагинацией и сортировкой')
async def search(
    query: str = Query(..., description='Поисковый запрос'),
    page: Page = Depends(get_page),
    sort: list[str] = Query(default=[], description='Поле для сортировки'),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmList]:
    films = await film_service.search(query=query, page=page, sort=sort)
    return [FilmList(**film.dict()) for film in films]


@router.get('/{film_id}',
            response_model=FilmDetails,
            summary='Информация о кинопроизведении',
            description='Детальная информация о кинопроизведении')
async def film_details(
    film_id: str = Path(..., description='ID кинопроизведения'),
    film_service: FilmService = Depends(get_film_service)
) -> FilmDetails:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=messages.FILM_NOT_FOUND)
    return FilmDetails(**film.dict())


@router.get('/',
            response_model=list[FilmList],
            summary='Список кинопроизведений',
            description='Список кинопропроизведений с фильтрацией '
                        'по актерам, режиссерам, сценаристам и жанрам '
                        'с пагинацией и сортировкой')
async def films(
    filter: Filter = Depends(get_filter),
    page: Page = Depends(get_page),
    sort: list[str] = Query(default=[], description='Поле для сортировки'),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmList]:
    films = await film_service.get(filter=filter, page=page, sort=sort)
    return [FilmList(**film.dict()) for film in films]
