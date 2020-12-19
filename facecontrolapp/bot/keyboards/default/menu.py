from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Распознвание'),
            KeyboardButton(text='Создать пользователя')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)