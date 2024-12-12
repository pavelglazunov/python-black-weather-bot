import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from config.config import Config
from src.keyboards.cities import SelectCityCallbackData, cities_keyboard
from src.keyboards.remove_city import remove_keyboard

router = Router()


@router.callback_query(SelectCityCallbackData.filter())
async def select_city(
        callback: types.CallbackQuery,
        callback_data: SelectCityCallbackData,
        state: FSMContext,
        config: Config,
):
    data = await state.get_data()
    cities = data.get("cities")
    frozen = data.get("frozen", {})
    city_index = callback_data.index

    now = datetime.datetime.utcnow()
    if now >= frozen.get(city_index, now):
        frozen.clear()

    if not frozen.get(city_index):
        frozen[city_index] = datetime.datetime.now() + datetime.timedelta(seconds=3)
        await state.update_data(frozen=frozen)
        await callback.answer("Чтобы удалить нажмите еще раз в течении 3 секунд")
        return

    cities.pop(city_index)
    frozen.clear()
    await state.update_data(frozen=frozen, cities=cities)
    await callback.message.edit_text(
        text=f"Добавлено {len(cities)}/{config.limits.max_cities}\n"
             "Ваш текущий маршрут:",
        reply_markup=cities_keyboard(cities, config.limits.max_cities),
    )
