from typing import Optional

from aioredis import Redis


redis: Optional[Redis] = None
"""Соединение с Redis."""


async def get_redis() -> Redis:
    """Получить соединение с Redis.
    
    Returns:
        Redis: соединение с Redis
    
    """
    return redis
