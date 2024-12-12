import aiohttp

from src.exceptions import APIFetchException


class RequestBase:
    base_url: str

    async def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        full_url = self.base_url + url
        params = {str(k): str(v) for k, v in params.items()}
        # try:
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        # except aiohttp.ClientConnectionError:
        #     raise APIFetchException("Не удалось подключиться к API сервису.")
        # except aiohttp.ClientResponseError as e:
        #     raise APIFetchException(f"Ошибка ответа от API: {e.status} - {e.message}")
        # except Exception as e:
        #     raise APIFetchException(f"Произошла непредвиденная ошибка: {str(e)}")
