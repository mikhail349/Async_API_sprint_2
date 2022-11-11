import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import films, genres, persons
from src.core import config
from src.core.logger import LOGGING
from src.db import redis, elastic

app = FastAPI(
    title=config.project_settings.PROJECT_NAME,
    description=config.project_settings.PROJECT_DESC,
    version=config.project_settings.PROJECT_VER,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    await redis.connect_redis()
    await elastic.connect_elastic()


@app.on_event('shutdown')
async def shutdown():
    await redis.close_redis()
    await elastic.close_elastic()


app.include_router(films.router, prefix='/api/v1/films',
                   tags=['Кинопроизведения'])
app.include_router(genres.router, prefix='/api/v1/genres',
                   tags=['Жанры'])
app.include_router(persons.router, prefix='/api/v1/persons',
                   tags=['Персоналии'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
