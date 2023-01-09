import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text

from app.keyboards import reply, inline
from app.data.db_api import get_all_users_devices, db_delete_device, db_get_device
from app.misc.classes import DeviceList
from app.misc.utils import get_now_formatted


logger = logging.getLogger(__name__)

async def command_my_devices(message: types.Message, state: FSMContext):
    await DeviceList.show_device_list.set()
    await message.answer(
        text='Список пристроїв:',
        reply_markup=reply.kb_back)

    user_id = (message.from_user.id, message.chat.id)[message.from_user.is_bot]

    for i, device in enumerate(await get_all_users_devices(user_id)):
        answer = (
            f'<b>{i+1}. {device.name}</b>\n'
            f'IP: {device.ip}\n'
            f'Статус: {device.status}\n'
            f'Не турбувати вночі: {("🔴", "🟢")[device.do_not_disturb]}\n'
            f'Сповіщати: {("🔴", "🟢")[device.notify]}\n'
            f'Остання зміна: {get_now_formatted(device.change_date)}'
        )
        await message.answer(answer,
                             reply_markup=await inline.device_keyboard(device_id=device.id))



async def delete_device(message: types.Message, device_id: int, state: FSMContext):
    user_id = (message.from_user.id, message.chat.id)[message.from_user.is_bot]
    try:
        if device := await db_get_device(int(device_id)):
            # await db_delete_device(device_id)
            logger.info(
                f'<delete_device> OK {user_id} deleted {device.name}'
            )
            answer = (
                f'Пристрій {device.name} був вдало видалений.'
            )
        else:
            logger.warning(
                f'<delete_device> OK {user_id} tried to delete {device_id}'
            )
            answer = 'Цей пристрій був видалений раніше'
    except Exception as err:
        logger.error(
            f'<delete_device> {user_id} get {err.args}'
        )
    await message.answer(answer)
    await command_my_devices(message, state)


async def navigate(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    action, device_id = callback_data.get('device_id').split('-')
    functions = {
        'del': delete_device,
        'change': 'change_device'
    }
    current_function = functions.get(action)

    await current_function(call.message, device_id, state)


def register_device_list(dp: Dispatcher):
    dp.register_message_handler(command_my_devices,
                                Text(equals='Мої пристрої',
                                     ignore_case=True),
                                state='*')
    dp.register_callback_query_handler(navigate,
                                       inline.cd.filter(),
                                       state='*'
                                       )
