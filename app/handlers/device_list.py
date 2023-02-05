import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.data.db_api import get_all_users_devices
from app.handlers.start import command_start
from app.keyboards import inline, reply
from app.misc.classes import DeviceList, get_device_view
from app.misc.exceptions import ConnectionErrorDB

logger = logging.getLogger(__name__)


async def command_my_device_list(message: types.Message, state: FSMContext):
    user_id = (message.from_user.id, message.chat.id)[message.from_user.is_bot]
    await DeviceList.show_device_list.set()

    try:
        device_list = await get_all_users_devices(user_id)
    except ConnectionErrorDB:
        await message.answer(
            '❌ Вибачте, зараз я не можу обробити цей запит.\n' +
            '✉️ Сповіщення про помилку відправлене адміністратору.\n'
            'Спробуйте повторити запит через деякий час.'
        )
        logger.error(
            f'{user_id} get ConnectionErrorDB'
        )
        return await command_start(message, state)
    except Exception as arr:
        logger.error(
            f'{user_id} get {arr.args}'
        )

    if not device_list:
        await message.answer(
            'Ви ще не зареєстрували жодного пристрою'
        )
        return await command_start(message, state)

    await message.answer(
        text='Список пристроїв:',
        reply_markup=reply.kb_back)

    try:
        for i, device in enumerate(device_list):
            answer = f'<b>{i+1}.</b> {await get_device_view(device)}'
            await message.answer(answer,
                                 reply_markup=await inline.create_device_keyboard(device_id=device.id))
        logger.info(
            f'{user_id} view the list of devices'
        )
    except ConnectionErrorDB:
        await message.answer(
            '❌ Вибачте, зараз я не можу обробити цей запит.\n' +
            '✉️ Сповіщення про помилку відправлене адміністратору.\n'
            'Спробуйте повторити запит через деякий час.'
        )
        logger.error(
            f'{user_id} get ConnectionErrorDB'
        )
        return await command_start(message, state)
    except Exception as arr:
        logger.error(
            f'{user_id} get {arr.args}'
        )


def register_device_list(dp: Dispatcher):
    dp.register_message_handler(command_my_device_list,
                                Text(equals='Мої пристрої',
                                     ignore_case=True),
                                state='*')
