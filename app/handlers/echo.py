import logging

from aiogram import Dispatcher, types


logger = logging.getLogger(__name__)


async def echo(message: types.Message):
    answer = (
        f'Ви ввели команду, яку я не розумію.\n\n' +
        f'<b>Використайте, будь ласка, <u>клавіатуру</u> ' +
        f'або перезавантажте бота командою /start</b>'
    )
    logger.info(
        f'<echo> OK {message.from_user.id} unsupported command {message.text}'
    )
    await message.answer(answer)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo, state='*')
