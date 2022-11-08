import asyncio
import logging

import aioredis
import backoff
import settings


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
async def wait_for_redis():
    """Метод для проверки готовности сервера redis."""
    redis = await aioredis.create_redis_pool(
        (settings.test_settings.REDIS_HOST, settings.test_settings.REDIS_PORT)
    )
    response = await redis.ping()
    if response:
        logging.info("Redis is ready!")
    else:
        logging.info("Waiting for redis")
        raise ConnectionError
    redis.close()
    await redis.wait_closed()


if __name__ == "__main__":
    asyncio.run(wait_for_redis())
