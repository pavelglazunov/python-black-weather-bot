from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config.config import Config
from src.api import AccuWeatherApi


class APIMiddleware(BaseMiddleware):
    def __init__(self, config: Config):
        super().__init__()
        self.api = AccuWeatherApi(config.api.openweather.key)

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        data["api"] = self.api

        return await handler(event, data)
