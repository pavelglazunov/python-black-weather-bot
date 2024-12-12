from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def start(message: types.Message):
    await message.answer("Доступные команды:\n"
                         "/start - запустить бота\n"
                         "/help - меню подсказок\n"
                         "/weather - проложить маршрут и узнать погоду")

