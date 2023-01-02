import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import CommandStart, Text

from app.keyboards import reply


logger = logging.getLogger(__name__)


async def command_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    answer = ''
    if not current_state:
        logger.info(
            f'<command_start> OK {message.from_user.id} started work')
        answer = (
            f'- Привітальна інформація\n'
        )
    answer += f'- Короткий опис, як працює чекер.'
    await message.answer(
        text=answer,
        reply_markup=reply.kb_start
    )


async def command_help(message: types.Message, state: FSMContext):
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


def register_start(dp: Dispatcher):
    dp.register_message_handler(command_start,
                                CommandStart(),
                                state='*')
    dp.register_message_handler(command_help,
                                Text(equals='Допомога', ignore_case=True),
                                state='*')
