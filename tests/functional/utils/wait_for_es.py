import asyncio
import logging

import backoff
from es_client import get_elastic


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
async def wait_for_es():
    """Метод для проверки готовности сервера elastic search."""
    es = await get_elastic()
    response = await es.ping()
    if response:
        logging.info("Elastic is ready!")
        await es.close()
    else:
        logging.info("Waiting for elastic")
        raise ConnectionError


if __name__ == "__main__":
    asyncio.run(wait_for_es())
