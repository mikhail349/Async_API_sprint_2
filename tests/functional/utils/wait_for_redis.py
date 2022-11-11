import backoff
from redis import Redis

from tests.functional import settings
from tests.functional.utils.logger import logger


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
def wait_for_redis():
    """Метод для проверки готовности сервера redis."""
    redis = Redis(settings.test_settings.REDIS_HOST,
                  settings.test_settings.REDIS_PORT)
    response = redis.ping()
    if response:
        logger.info("Redis is ready!")
    else:
        logger.info("Waiting for redis")
        raise ConnectionError
    redis.close()


if __name__ == "__main__":
    wait_for_redis()
