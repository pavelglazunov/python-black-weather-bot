from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, CallbackData


class SelectDaysCountCallbackData(CallbackData, prefix="days-count"):
    days: int


days_count_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=str(days),
            callback_data=SelectDaysCountCallbackData(days=days).pack()
        )
    ] for days in (1, 5, 10, 15)
])
