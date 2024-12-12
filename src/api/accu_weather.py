from src.api.base import RequestBase
from src.api.interface import WeatherDataInterface, WeatherData, DayWeather
from src.exceptions import APIFetchException


class AccuWeatherApi(WeatherDataInterface, RequestBase):
    base_url = "http://dataservice.accuweather.com"

    def __init__(self, token: str):
        self.token = token
        super().__init__()

    async def get_location(self, city: str) -> str:

        data = await self.get(
            url="/locations/v1/cities/search",
            params={
                "apikey": self.token,
                "q": city,
                "details": True,
            }
        )
        return data[0].get("Key")

    async def get_weather(self, city: str, days: int) -> WeatherData:
        try:
            location = await self.get_location(city)
        except Exception as e:
            raise APIFetchException(f"Город {city} не найден")

        url = f"/forecasts/v1/daily/{days}day/{location}"
        data = await self.get(
            url=url,
            params={
                "apikey": self.token,
                "details": True,
                "metric": True,
            })

        try:
            forecasts = []
            for day in data.get("DailyForecasts", []):
                min_temperature = day.get("Temperature", {}).get("Minimum", {}).get("Value", 0)
                max_temperature = day.get("Temperature", {}).get("Maximum", {}).get("Value", 0)
                forecasts.append(
                    DayWeather(
                        date=day.get("Date"),
                        temperature=(min_temperature + max_temperature) / 2,
                        rain_probability=day.get("Day", {}).get("PrecipitationProbability", 0),
                        winter_speed=day.get("Day", {}).get("Wind", {}).get("Speed", {}).get(
                            "Value", 0)
                    ),
                )

            return WeatherData(days=forecasts)
        except Exception:
            raise APIFetchException(f"не удалось распаковать данные от сервера")
