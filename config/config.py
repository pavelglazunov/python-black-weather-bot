import logging
from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv


# logging
def init_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("app.log")


@dataclass
class Bot:
    token: str


@dataclass
class Limits:
    max_cities: int


@dataclass
class API:
    key: str


@dataclass
class ApiManager:
    openweather: API


@dataclass
class Config:
    bot: Bot
    limits: Limits
    api: ApiManager


def load_config() -> Config:
    load_dotenv()
    return Config(
        bot=Bot(
            token=getenv("TOKEN"),
        ),
        limits=Limits(
            max_cities=int(getenv("LIMIT_CITY_COUNT")),
        ),
        api=ApiManager(
            openweather=API(
                key=getenv("API_OPENWEATHER_KEY"),
            ),
        ),
    )
