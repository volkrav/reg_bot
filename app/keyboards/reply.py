from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


'''************************ Стартове вікно ************************'''


kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Зареєструвати пристрій'),
            KeyboardButton(text='Мої пристрої')
        ],
        [
            KeyboardButton(text='Допомога')
        ]
    ],
    resize_keyboard=True
)
