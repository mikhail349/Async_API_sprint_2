import aiohttp

from tests.functional.settings import test_settings


class APIClient:
    """Клиент для работы с api."""
    def __init__(self):
        self.url = test_settings.API

    async def get(self, endpoint: str, **params):
        """Выплоняет get запрос на указанный endpoint с параметрами."""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + endpoint, **params) as resp:
                return await resp.json(), resp.status
