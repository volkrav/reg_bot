import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text

from app.keyboards import reply, inline
from app.data.db_api import get_all_users_devices, db_delete_device, db_get_device
from app.misc.classes import DeviceList, get_device_view
from app.misc.utils import get_now_formatted


logger = logging.getLogger(__name__)


async def command_my_devices(message: types.Message, state: FSMContext):
    await DeviceList.show_device_list.set()
    await message.answer(
        text='Список пристроїв:',
        reply_markup=reply.kb_back)

    user_id = (message.from_user.id, message.chat.id)[message.from_user.is_bot]

    for i, device in enumerate(await get_all_users_devices(user_id)):
        answer = f'<b>{i+1}.</b> {await get_device_view(device)}'
        await message.answer(answer,
                             reply_markup=await inline.device_keyboard(device_id=device.id))


def register_device_list(dp: Dispatcher):
    dp.register_message_handler(command_my_devices,
                                Text(equals='Мої пристрої',
                                     ignore_case=True),
                                state='*')
