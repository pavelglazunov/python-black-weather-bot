"""
Так на основном апи ограниченное кол-во запросов, было принять волевое решение
сделать интерфейсы и тестировать все на open weather, после чего просто поменять токен и ссылку
"""
import datetime
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class DayWeather:
    date: datetime.datetime
    temperature: float
    rain_probability: float
    winter_speed: float


@dataclass
class WeatherData:
    days: list[DayWeather]


class WeatherDataInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_weather(self, city: str, days: int) -> WeatherData:
        pass
