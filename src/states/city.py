from aiogram.fsm.state import State, StatesGroup


class StartCitiesInput(StatesGroup):
    city1 = State()
    city2 = State()

class InputCityState(StatesGroup):
    city = State()
