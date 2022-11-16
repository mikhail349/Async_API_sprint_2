from typing import Optional, Any

from aioredis import Redis
import backoff

from src.core import config
from src.storages.base import CacheStorage


class RedisStorage(CacheStorage):
    """Класс для работы с кэшом Redis.

    Args:
        redis: соединение с Redis

    """
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @backoff.on_exception(backoff.expo,
                          exception=OSError,
                          max_time=config.redis_settings.BACKOFF_MAX_TIME)
    async def get(self, key: str) -> Optional[Any]:
        """Получить данные по ключу из кэша.

        Args:
            key: ключ

        Returns:
            Optional[Any]: данные

        """
        return await self.redis.get(key)

    @backoff.on_exception(backoff.expo,
                          exception=OSError,
                          max_time=config.redis_settings.BACKOFF_MAX_TIME)
    async def put(self, key: str, value: Any):
        """Записать данные в кэш.

        Args:
            key: ключ
            value: данные

        """
        await self.redis.set(
            key, value,
            expire=config.redis_settings.CACHE_EXPIRE_IN_SECONDS)
