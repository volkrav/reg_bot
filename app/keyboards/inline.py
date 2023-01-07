from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cd = CallbackData('action', 'device_id')

def make_callbackdata(action: str, device_id: str) -> CallbackData:
    return cd.new(device_id=f'{action}-{device_id}')

async def device_keyboard(device_id) -> InlineKeyboardMarkup:

    markup = InlineKeyboardMarkup()
    button_change_text = InlineKeyboardButton(
        text='Змінити',
        callback_data=make_callbackdata('change', device_id)
    )
    button_del_text = InlineKeyboardButton(
        text='Видалити',
        callback_data=make_callbackdata('del', device_id)
    )

    return markup.row(
        button_change_text,
        button_del_text
    )
