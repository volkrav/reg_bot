import asyncio
import datetime
import os

import pytz
from aiogram import types

from app.keyboards import reply

TZ = pytz.timezone("Europe/Kiev")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')


async def get_now_datetime() -> datetime.datetime:
    now = datetime.datetime.now(TZ).replace(tzinfo=None)
    return now


async def get_now_formatted(dt: datetime.datetime = None) -> str:
    if not dt:
        dt = await get_now_datetime()
    return dt.strftime("%H:%M %d.%m.%Y")


async def get_now_datetime_minus_an_hour():
    now_minus_hour = await get_now_datetime() - datetime.timedelta(hours=1)
    return now_minus_hour


async def get_user_id(message: types.Message):
    return message.chat.id if message.from_user.is_bot else message.from_user.id


async def check_ip(ip: str = None) -> bool:
    if not isinstance(ip, str):
        return False
    octets = ip.split('.')
    if len(octets) != 4:
        return False
    for octet in octets:
        if (not octet.isdigit()) or \
                (int(octet) < 0 or int(octet) > 255):
            return False
    return True


async def reply_not_validation_ip(message: types.Message):
    await message.reply(
        text='‼️ Невірний формат IP адреси ‼️\n\n' +
        'IP-адреси є набір з чотирьох чисел, розділених крапками, ' +
        'наприклад, 192.158.1.38. Кожне число цього набору належить ' +
        'інтервалу від 0 до 255. Таким чином, повний діапазон ' +
        'IP-адресації – це адреси від 0.0.0.0 до 255.255.255.255\n\n'
        'Введіть, будь ласка, коректне значення IP пристрою  ⤵️',
        reply_markup=reply.kb_cancel
    )


async def check_name(name: str = None) -> bool:
    return isinstance(name, str) and (len(name) < 50)


async def reply_not_validation_name(message: types.Message):
    await message.reply(
        text='‼️ Назва не повинна перевищувати 50 символів ‼️\n\n' +
        'Будь ласка, придумайте та введіть коротшу назву пристрою  ⤵️',
        reply_markup=reply.kb_cancel
    )


async def get_text_from_file(filename: str) -> str | None:
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(
            None, _sync_open_file_for_read, STATIC_DIR, filename)
    except Exception as err:
        return None


def _sync_open_file_for_read(STATIC_DIR: str, filename: str) -> str:
    with open(os.path.join(STATIC_DIR, filename)) as data:
        return data.read()
