import logging

import backoff
from tests.functional.utils.es_client import get_elastic


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
def wait_for_es():
    """Метод для проверки готовности сервера elastic search."""
    es = get_elastic()
    response = es.ping()
    if response:
        logging.info("Elastic is ready!")
        es.close()
    else:
        logging.info("Waiting for elastic")
        raise ConnectionError


if __name__ == "__main__":
    wait_for_es()
