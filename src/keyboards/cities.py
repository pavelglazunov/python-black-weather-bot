from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, CallbackData


class SelectCityCallbackData(CallbackData, prefix="select-city"):
    index: int


class AddCityCallbackData(CallbackData, prefix="add-city"):
    after_index: int


class ProcessWeatherCallbackData(CallbackData, prefix="process"):
    pass


def cities_keyboard(cities: list[str], limit: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    kb.inline_keyboard.append([
                                  InlineKeyboardButton(
                                      text="+",
                                      callback_data=AddCityCallbackData(after_index=0).pack(),
                                  )
                              ] * (len(cities) < limit))

    for i, city in enumerate(cities, 1):
        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text=city,
                callback_data=SelectCityCallbackData(index=i - 1).pack(),
            ),
        ])
        kb.inline_keyboard.append([
                                      InlineKeyboardButton(
                                          text="+",
                                          callback_data=AddCityCallbackData(after_index=i).pack(),
                                      )
                                  ] * (len(cities) < limit))

    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text="🚀 Узнать погоду!",
            callback_data=ProcessWeatherCallbackData().pack(),
        )
    ])

    return kb
