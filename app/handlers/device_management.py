import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text

from app.handlers.device_list import command_my_device_list
from app.keyboards import reply, inline
from app.data.db_api import get_all_users_devices, db_delete_device, db_get_device
from app.misc.classes import DeviceList, get_device_view, Device
from app.misc.utils import get_now_formatted, get_user_id


logger = logging.getLogger(__name__)


async def delete_device(message: types.Message, state: FSMContext, device: Device):
    user_id = await get_user_id(message)
    try:
        if device:
            await db_delete_device(device.id)
            logger.info(
                f'<delete_device> OK {user_id} deleted {device.name}'
            )
            answer = (
                f'Пристрій {device.name} був вдало видалений.'
            )
        else:
            logger.warning(
                f'<delete_device> OK {user_id} tried to delete a deleted device'
            )
            answer = 'Цей пристрій був видалений раніше'
    except Exception as err:
        logger.error(
            f'<delete_device> {user_id} get {err.args}'
        )
    await message.answer(answer)
    await command_my_device_list(message, state)


async def change_device(message: types.Message, state: FSMContext, device: Device):
    user_id = await get_user_id(message)
    if not device:
        logger.warning(
            f'<change_device> OK {user_id} tried to change a deleted device'
        )
        await message.answer('Цей пристрій був видалений раніше')
        return await command_my_device_list(message, state)
    await DeviceList.change_device.set()
    answer = '✏️ Пристрій:\n\n' + await get_device_view(device)
    await message.answer(
        text=answer + '\n\n' + 'Що будемо змінювати? ⤵️',
        reply_markup=reply.kb_change
        )
    ...


async def navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    action, device_id = callback_data.get('device_id').split('-')
    functions = {
        'del': delete_device,
        'change': change_device,
    }
    current_function = functions.get(action)
    device = await db_get_device(device_id)

    await current_function(call.message, state, device)


def register_device_management(dp: Dispatcher):
    dp.register_callback_query_handler(navigate,
                                       inline.cd.filter(),
                                       state='*'
                                       )
