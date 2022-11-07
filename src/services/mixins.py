from dataclasses import dataclass
from typing import Optional

from aioredis import Redis
from pydantic import BaseModel

from src.core import config


@dataclass
class RedisCacheMixin:
    """Миксин, содержащий методы для работы с кэшем на базе Redis.

    Args:
        redis: соединение с Redis
        model: класс модели объекта

    """
    redis: Redis
    model: BaseModel = BaseModel

    async def get_obj_from_cache(self, obj_id: str) -> Optional[model]:
        """Получить объект по ID из кэша.

        Args:
            obj_id: ID объекта

        Returns:
            Optional[model]: объект

        """
        data = await self.redis.get(obj_id)
        if not data:
            return None

        obj = self.model.parse_raw(data)
        return obj

    async def put_obj_to_cache(self, obj: model):
        """Записать объект в кэш.

        Args:
            obj: объект

        """
        await self.redis.set(
            obj.id, obj.json(),
            expire=config.redis_settings.CACHE_EXPIRE_IN_SECONDS)

    async def get_objects_from_cache(self, key: str) -> list[model]:
        """Получить список объектов из кэша.

        Args:
            key: ключ

        Returns:
            list[model]: список объектов

        """
        data = await self.redis.get(key)
        if not data:
            return []

        json_loads = self.model.Config.json_loads
        objects = json_loads(data)
        objects = [self.model.parse_obj(obj) for obj in objects]
        return objects

    async def put_objects_to_cache(self, key: str, objects: list[model]):
        """Записать список объектов в кэш.

        Args:
            key: ключ
            objects: список объектов

        """
        json_dumps = self.model.Config.json_dumps
        value = json_dumps([obj.dict() for obj in objects], default=str)
        await self.redis.set(
            key, value, expire=config.redis_settings.CACHE_EXPIRE_IN_SECONDS)
