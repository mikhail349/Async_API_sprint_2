import aiohttp
from tests.functional.settings import test_settings


class APIClient:

    def __init__(self):
        self.url = test_settings.API

    async def get(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + "genres") as resp:
                return await resp.json()

    async def get_by_id(self, obj_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + f"genres/{obj_id}") as resp:
                return await resp.json(), resp.status
