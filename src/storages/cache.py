from src.db.redis import get_redis
from src.storages.redis import RedisStorage
from src.storages.base import CacheStorage


async def get_cache_storage() -> CacheStorage:
    """Получить инстанс класса хранилища кеша.

    Returns:
        CacheStorage: Класс хранилища кеша

    """
    redis = await get_redis()
    return RedisStorage(redis=redis)
