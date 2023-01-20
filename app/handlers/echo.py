import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.keyboards import reply

logger = logging.getLogger(__name__)


async def echo(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    match (current_state, None):
        case curr_state, _ if not curr_state \
                or curr_state.split(':')[0] in ('Start',):
            markup = reply.kb_start
        case curr_state, _ if curr_state.split(':')[0] in ('NeedHelp',):
            markup = reply.kb_help
        case "DeviceAction:change_device", _:
            markup = reply.kb_change
        case curr_state, _ if curr_state.split(':')[0] in ('DeviceList',):
            markup = reply.kb_back
        case curr_state, _ if curr_state == 'DeviceAction:del_device':
            markup = reply.kb_yes_or_no
        case curr_state, _ if curr_state in ('DeviceChange:do_not_disturb',
                                             'DeviceChange:notify'):
            markup = reply.kb_on_off_cancel
        # case _:DeviceList
        #     print(f"_")

    answer = (
        f'Ви ввели команду, яку я не розумію.\n\n' +
        f'<b>Використайте, будь ласка, <u>клавіатуру</u> ' +
        f'або перезавантажте бота командою /start</b>'
    )
    logger.warning(
        f'{message.from_user.id} unsupported command {message.text}'
    )
    await message.answer(
        text=answer,
        reply_markup=markup
    )


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo, state='*')
