from functools import lru_cache
from dataclasses import dataclass

from fastapi import Depends
from pydantic import BaseModel

from src.db.redis import get_redis_storage, RedisStorage
from src.models import person
from src.services.base import BaseService
from src.storages.base import DataStorage
from src.storages.persons import get_data_storage


@dataclass
class PersonService(BaseService):
    """Сервис персоны."""
    model: BaseModel = person.Person
    cache_key_prefix: str = 'persons'


@lru_cache()
def get_person_service(
        redis_storage: RedisStorage = Depends(get_redis_storage),
        data_storage: DataStorage = Depends(get_data_storage),
) -> PersonService:
    return PersonService(redis_storage=redis_storage,
                         data_storage=data_storage)
