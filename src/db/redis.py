from typing import Optional

from aioredis import Redis, create_redis_pool
import backoff

from src.core.config import redis_settings


redis: Optional[Redis] = None
"""Соединение с Redis."""


async def get_redis() -> Redis:
    """Получить соединение с Redis.

    Returns:
        Redis: соединение с Redis

    """
    return redis


@backoff.on_exception(backoff.expo,
                      exception=OSError,
                      max_time=redis_settings.BACKOFF_MAX_TIME)
async def connect_redis() -> Redis:
    """Установить соединение с Redis.

    Returns:
        Redis: соединение с Redis

    """
    global redis
    redis = await create_redis_pool(
        (redis_settings.REDIS_HOST, redis_settings.REDIS_PORT),
        minsize=10,
        maxsize=20
    )


async def close_redis():
    """Закрыть соединение с Redis."""
    redis = await get_redis()
    redis.close()
    await redis.wait_closed()
