import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.handlers.start import command_start
from app.handlers.device_list import command_my_device_list
from app.handlers.device_management import select_field_to_change


logger = logging.getLogger(__name__)


async def command_back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    logger.info(
        f'<command_back> OK {message.from_user.id} is {current_state}')
    current_function = await _get_current_function(current_state)
    await current_function(message, state)


async def _get_current_function(current_state: str):
    match (current_state, None):
        case state, _ if (not state) or\
                state.split(':')[0] in ('Start',
                                           'CheckIn',
                                           'DeviceList',
                                           'NeedHelp'):
            return command_start
        case 'DeviceAction:change_device', _:
            return command_my_device_list
        case state, _ if state.split(':')[0] == 'DeviceChange':
            return select_field_to_change


def register_back(dp: Dispatcher):
    dp.register_message_handler(command_back,
                                Text(equals=[
                                    '⬅️ Назад',
                                    '❌ Скасувати'
                                ],
                                    ignore_case=True),
                                state='*')
