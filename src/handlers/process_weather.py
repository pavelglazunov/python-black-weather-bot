from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.api import WeatherDataInterface
from src.keyboards.cities import ProcessWeatherCallbackData
from src.keyboards.input_days import days_count_keyboard, SelectDaysCountCallbackData
from src.exceptions import APIFetchException
router = Router()


@router.callback_query(ProcessWeatherCallbackData.filter())
async def process_weather(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cities = data.get("cities", [])
    if not cities:
        await callback.answer("Необходимо указать хотя бы один город")
        return

    await callback.message.edit_text(
        text="Выберите на какое кол-во дней узнать погоду:",
        reply_markup=days_count_keyboard,
    )


@router.callback_query(SelectDaysCountCallbackData.filter())
async def input_days_and_process(
        callback: types.CallbackQuery,
        callback_data: SelectDaysCountCallbackData,
        state: FSMContext,
        api: WeatherDataInterface,
):
    await callback.message.edit_text(text="Получение данных, пожалуйста подождите...")

    days = callback_data.days

    data = await state.get_data()
    cities = data.get("cities")

    content = "Погода в городах:\n"

    for city in cities:
        try:
            weather_data = await api.get_weather(city, days)
            content += f"{city}:\n"
            for day in weather_data.days:
                content += (f"{day.date.strftime('%d-%m-%Y')}: \n"
                            f"- Температура: {day.temperature}\n"
                            f"- Осадки: {day.rain_probability}\n"
                            f"- Скорость ветра: {day.winter_speed}\n"
                            f"\n")
        except APIFetchException as err:
            content += ("Ошибка: \n"
                        f"{err.message}\n\n")

    await callback.message.edit_text(text=content)

