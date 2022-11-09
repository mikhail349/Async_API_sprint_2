import logging

from redis import Redis
import backoff
from tests.functional import settings


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
def wait_for_redis():
    """Метод для проверки готовности сервера redis."""
    redis = Redis(settings.test_settings.REDIS_HOST,
                  settings.test_settings.REDIS_PORT)
    response = redis.ping()
    if response:
        logging.info("Redis is ready!")
    else:
        logging.info("Waiting for redis")
        raise ConnectionError
    redis.close()


if __name__ == "__main__":
    wait_for_redis()
