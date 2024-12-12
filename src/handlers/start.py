from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.services import aio

router = Router()


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await aio.clear_state_with_save_data(state)
    await message.answer("✨ Привет!\n"
                         "В данном боте ты можешь узнать погоду в любом городе, который ты "
                         "хотел бы посетить\n\n"
                         "Можешь использовать /weather чтобы начать или /help чтобы посмотреть"
                         " доступные команды")
