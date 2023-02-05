import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.config import Config
from app.keyboards import reply
from app.misc.classes import NeedHelp
from app.misc.utils import get_text_from_file

logger = logging.getLogger(__name__)


async def command_help(message: types.Message, state: FSMContext):
    await NeedHelp.start.set()
    logger.info(
        f'{message.from_user.id} open help'
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
        f'{message.from_user.id} looks how_to_register'
    )
    answer = await get_text_from_file('how_to_register.txt')

    await message.answer(text=answer)


async def command_how_it_work(message: types.Message, state: FSMContext):
    await NeedHelp.how_work.set()
    logger.info(
        f'{message.from_user.id} looks how_it_work'
    )
    answer = await get_text_from_file('how_it_work.txt')
    config: Config = message.bot.get('config')
    photo_id = config.tg_bot.photo_id
    await message.answer(text=answer)
    await message.answer_photo(photo_id)


def register_help(dp: Dispatcher):
    dp.register_message_handler(command_help,
                                Text(equals=[
                                    'Допомога',
                                    '/help'], ignore_case=True),
                                state='*')
    dp.register_message_handler(command_how_to_register,
                                Text(equals='Як зареєструватися',
                                     ignore_case=True),
                                state='*')
    dp.register_message_handler(command_how_it_work,
                                Text(equals='Як працює бот',
                                     ignore_case=True),
                                state='*')
