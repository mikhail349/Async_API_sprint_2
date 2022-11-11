import backoff

from tests.functional.utils.es_client import get_elastic
from tests.functional.utils.logger import logger


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
def wait_for_es():
    """Метод для проверки готовности сервера elastic search."""
    es = get_elastic()
    response = es.ping()
    if response:
        logger.info("Elastic is ready!")
        es.close()
    else:
        logger.info("Waiting for elastic")
        raise ConnectionError


if __name__ == "__main__":
    wait_for_es()
