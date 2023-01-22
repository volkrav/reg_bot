from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


'''************************ Окремі кнопки ************************'''

btn_back = KeyboardButton(text='⬅️ Назад')
btn_cancel = KeyboardButton(text='❌ Скасувати')


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


'''************************ Змінити пристрій ************************'''
kb_change = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назву'),
            KeyboardButton(text='IP'),
        ],
        [
            KeyboardButton(text='Не турбувати'),
            KeyboardButton(text='Сповіщати'),
        ],
        [
            btn_back,
        ],
    ],
    resize_keyboard=True
)


'''************************ Так Ні ************************'''

kb_yes_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Так')
        ],
        [
            KeyboardButton(text='Ні')
        ],
    ],
    resize_keyboard=True
)


'''************************ Так Ні ************************'''

kb_on_off_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🟢 увімкнено')
        ],
        [
            KeyboardButton(text='🔴 вимкнено')
        ],
        [
            btn_cancel
        ],
    ],
    resize_keyboard=True
)


'''************************ Скасувати ************************'''

kb_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [btn_cancel]
    ],
    resize_keyboard=True
)


'''************************ Назад ************************'''

kb_back = ReplyKeyboardMarkup(
    keyboard=[
        [btn_back]
    ],
    resize_keyboard=True
)
