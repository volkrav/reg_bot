import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text

from app.misc.classes import NeedHelp
from app.keyboards import reply


logger = logging.getLogger(__name__)


async def command_help(message: types.Message, state: FSMContext):
    await NeedHelp.start.set()
    logger.info(
        f'<command_help> OK {message.from_user.id} open help'
    )
    answer = (
        f'Будь ласка, оберіть потрібний розділ ⤵️'
    )
    await message.answer(
        text=answer,
        reply_markup=reply.kb_help
    )

async def command_how_to_register(message: types.Message, state: FSMContext):
    await NeedHelp.how_register.set()

    logger.info(
        f'<command_how_to_register> OK {message.from_user.id} looks how_to_register'
    )
    answer = (
        f'Детальна інструкція як зареєструватися'
    )
    await message.answer(text=answer)


async def command_how_it_work(message: types.Message, state: FSMContext):
    await NeedHelp.how_work.set()
    logger.info(
        f'<command_how_it_work> OK {message.from_user.id} looks how_it_work'
    )
    answer = (
        f'Детальний опис як працює чеккер'
    )
    await message.answer(text=answer)



def register_help(dp: Dispatcher):
    dp.register_message_handler(command_help,
                            Text(equals='Допомога', ignore_case=True),
                            state='*')
    dp.register_message_handler(command_how_to_register,
                                Text(equals='Як зареєструватися',
                                     ignore_case=True),
                                state='*')
    dp.register_message_handler(command_how_it_work,
                                Text(equals='Як працює бот',
                                     ignore_case=True),
                                state='*')
