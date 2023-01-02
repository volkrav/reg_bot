from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

'''************************ Окремі кнопки ************************'''

btn_back = KeyboardButton(text='⬅️ Назад')

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


'''************************ Вікно з допомогою ************************'''
kb_help = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Як зареєструватися')
        ],
        [
            KeyboardButton(text='Як працює бот')
        ],
        [
            btn_back
        ]
    ],
    resize_keyboard=True
)
