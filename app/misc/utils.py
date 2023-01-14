import datetime

import pytz
from aiogram import types

TZ = pytz.timezone("Europe/Kiev")


def get_now_datetime() -> datetime.datetime:
    now = datetime.datetime.now(TZ)
    return now


def get_now_formatted(dt: datetime.datetime = None) -> str:
    if not dt:
        dt = get_now_datetime()
    return dt.strftime("%H:%M:%S %d-%m-%Y")


def is_day() -> bool:
    return 7 < datetime.datetime.now(TZ).hour < 24


async def is_device_exists(message: types.Message):
    ...


async def get_user_id(message: types.Message):
    return message.chat.id if message.from_user.is_bot else message.from_user.id


async def check_ip(ip: str) -> bool:
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
