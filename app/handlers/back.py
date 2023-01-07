import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.handlers.start import command_start


logger = logging.getLogger(__name__)


async def command_back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    logger.info(
        f'<command_back> OK {message.from_user.id} is {current_state}')
    current_function = await _get_current_function(current_state)
    await current_function(message, state)


async def _get_current_function(current_state: FSMContext):
    functions = {
        None: command_start,
        'Start:free': command_start,
        'CheckIn:canceled': command_start,  # TODO!
        'DeviceList:show_device_list': command_start,
    }
    return functions.get(current_state, command_start)


def register_back(dp: Dispatcher):
    dp.register_message_handler(command_back,
                                Text(equals=[
                                    '⬅️ Назад',
                                    '❌ Скасувати'
                                ],
                                    ignore_case=True),
                                state='*')
