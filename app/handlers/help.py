import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text

from app.handlers.start import command_start


logger = logging.getLogger(__name__)


async def command_how_to_register(message: types.Message, state: FSMContext):
    logger.info(
        f'<command_how_to_register> OK {message.from_user.id} looks how_to_register'
    )
    answer = (
        f'Детальна інструкція як зареєструватися'
    )
    await message.answer(text=answer)


async def command_how_it_work(message: types.Message, state: FSMContext):
    logger.info(
        f'<command_how_it_work> OK {message.from_user.id} looks how_it_work'
    )
    answer = (
        f'Детальний опис як працює чеккер'
    )
    await message.answer(text=answer)


async def command_back(message: types.Message, state: FSMContext):
    await command_start(message, state)


def register_help(dp: Dispatcher):
    dp.register_message_handler(command_how_to_register,
                                Text(equals='Як зареєструватися',
                                     ignore_case=True),
                                state='*')
    dp.register_message_handler(command_how_it_work,
                                Text(equals='Як працює бот',
                                     ignore_case=True),
                                state='*')
    dp.register_message_handler(command_back,
                                Text(equals='⬅️ Назад', ignore_case=True),
                                state='*')
