from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Path, HTTPException

from src.api.v1.query_params.base import Page, get_page
from src.api.v1.models.genre import Genre
from src.services.genre import GenreService, get_genre_service
from src.core.messages import GENRE_NOT_FOUND

router = APIRouter()


@router.get('/search',
            response_model=list[Genre],
            summary='Поиск жанров',
            description='Полнотекстовый поиск жанров с пагинацией')
async def search(
        query: str = Query(..., description='Поисковый запрос'),
        page: Page = Depends(get_page),
        sort: list[str] = Query(default=[],
                                description='Поле для сортировки'),
        genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    return await genre_service.search(query=query, page=page, sort=sort)


@router.get("/",
            response_model=list[Genre],
            summary='Список жанров',
            description='Список жанров с пагинацией')
async def genres(
    page: Page = Depends(get_page),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    return await genre_service.get(page=page)


@router.get("/{genre_id}",
            response_model=Genre,
            summary='Информация о жанре',
            description='Детальная информация о жанре')
async def genre_details(
    genre_id: str = Path(..., description='ID жанра'),
    genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=GENRE_NOT_FOUND)
    return genre
