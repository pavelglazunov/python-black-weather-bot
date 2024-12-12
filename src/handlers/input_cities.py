from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config.config import Config
from src.keyboards.cities import cities_keyboard
from src.services import aio
from src.states import InputCityState

router = Router()


@router.message(Command("weather"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите начальный город:")
    await state.update_data(cities=[], insert_after=0)
    await state.set_state(InputCityState.city)


@router.message(InputCityState.city, F.text)
async def input_city(
        message: types.Message,
        state: FSMContext,
        config: Config,
):
    data = await state.get_data()
    cities = data.get("cities", [])
    insert_to = data.get("insert_after", 0)

    city_name = message.text

    cities.insert(insert_to, city_name)
    await state.update_data(cities=cities)

    if len(cities) == 1:
        await message.answer("Введите конечный город:")
        await state.update_data(insert_to=1)
        return

    await aio.clear_state_with_save_data(state)
    await message.answer(
        text=f"Добавлено {len(cities)}/{config.limits.max_cities}\n"
             "Ваш текущий маршрут:",
        reply_markup=cities_keyboard(cities, config.limits.max_cities),
    )
