from typing import NamedTuple

from aiogram.dispatcher.filters.state import StatesGroup, State

from app.misc.utils import get_now_formatted, datetime, get_now_datetime

class Start(StatesGroup):
    free = State()

class NeedHelp(StatesGroup):
    start = State()
    how_register = State()
    how_work = State()

class CheckIn(StatesGroup):
    name = State()
    ip = State()
    disturb = State()
    canceled = State()

class DeviceList(StatesGroup):
    show_device_list = State()

class DeviceAction(StatesGroup):
    del_device = State()
    change_device = State()

class DeviceChange(StatesGroup):
    name = State()
    ip = State()
    disturb = State()
    notify = State()
    canceled = State()

class Device(NamedTuple):
    id: int | None
    name: str
    ip: str
    status: str
    do_not_disturb: bool
    notify: bool
    change_date: datetime.datetime | str
    user_id: int


async def create_device(data: dict) -> Device:
    return Device(
        id = data.get('id', None),
        name = data.get('name'),
        ip = data.get('ip'),
        status = data.get('status', ''),
        do_not_disturb = data.get('do_not_disturb'),
        notify = data.get('notify', True),
        change_date = data.get('change_date', get_now_datetime()),
        user_id = data.get('user_id')
    )

async def get_device_view(device: Device) -> str:
            return (
            f'<b>{device.name}</b>\n'
            f'IP: {device.ip}\n'
            f'Статус: {device.status}\n'
            f'Не турбувати вночі: {("🔴", "🟢")[device.do_not_disturb]}\n'
            f'Сповіщати: {("🔴", "🟢")[device.notify]}\n'
            f'Остання зміна: {get_now_formatted(device.change_date)}'
        )
