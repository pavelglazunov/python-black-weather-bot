from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, CallbackData


class RemoveCityCallbackData(CallbackData, prefix="remove"):
    index: int


class HomoCallbackData(CallbackData, prefix="home"):
    pass


def remove_keyboard(index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Удалить",
                callback_data=RemoveCityCallbackData(index=index).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🏠 Назад",
                callback_data=HomoCallbackData().pack(),
            )
        ]
    ])
