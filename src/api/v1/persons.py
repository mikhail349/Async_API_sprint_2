from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Path, HTTPException

from src.api.v1.query_params.base import Page, get_page
from src.api.v1.query_params.persons import Filter, get_filter
from src.api.v1.models.person import Person
from src.services.person import PersonService, get_person_service
from src.core.messages import PERSON_NOT_FOUND

router = APIRouter()


@router.get('/search',
            response_model=list[Person],
            summary='Поиск персоналий',
            description='Полнотекстовый поиск по персоналиям '
                        'с пагинацией и сортировкой')
async def search(
        query: str = Query(..., description='Поисковый запрос'),
        page: Page = Depends(get_page),
        sort: list[str] = Query(None, description='Поле для сортировки'),
        genre_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    return await genre_service.search(query=query, page=page, sort=sort)


@router.get("/{person_id}",
            response_model=Person,
            summary='Информация о персоне',
            description='Детальная информация о персоне')
async def person_details(
        person_id: str = Path(..., description='ID персоны'),
        person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PERSON_NOT_FOUND)
    return person


@router.get("/",
            response_model=list[Person],
            summary='Список персоналий',
            description='Список персоналий с пагинацией и сортировкой')
async def persons(
        filter: Filter = Depends(get_filter),
        page: Page = Depends(get_page),
        sort: list[str] = Query(None, description='Поле для сортировки'),
        person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    return await person_service.get(page=page, sort=sort, filter=filter)
