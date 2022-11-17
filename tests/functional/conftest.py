import asyncio

import pytest

from tests.functional.src.lib.api_client import APIClient


pytest_plugins = ("tests.functional.fixtures.es",
                  "tests.functional.fixtures.person",
                  "tests.functional.fixtures.genre",
                  "tests.functional.fixtures.film")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def api_client():
    """Объект клиента для работы с API."""
    yield APIClient()
