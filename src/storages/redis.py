from typing import Optional, Any

from aioredis import Redis

from src.core import config
from src.db.redis import get_redis


class RedisStorage:
    """Класс для работы с кэшом Redis.

    Args:
        redis: соединение с Redis

    """
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get(self, key: str) -> Optional[Any]:
        """Получить данные по ключу из кэша.

        Args:
            key: ключ

        Returns:
            Optional[Any]: данные

        """
        return await self.redis.get(key)

    async def put(self, key: str, value: Any):
        """Записать данные в кэш.

        Args:
            value: данные

        """
        await self.redis.set(
            key, value,
            expire=config.redis_settings.CACHE_EXPIRE_IN_SECONDS)


async def get_redis_storage() -> RedisStorage:
    """Получить инстанс класса хранилища Redis

    Returns:
        RedisStorage: Класс хранилища Redis

    """
    redis = await get_redis()
    return RedisStorage(redis=redis)
