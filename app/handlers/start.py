import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from app.keyboards import reply
from app.misc.classes import Start

logger = logging.getLogger(__name__)


async def command_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    answer = ''
    if not current_state:
        logger.info(
            f'<command_start> OK {message.from_user.id} started work')
        answer = (
            f'- Привітальна інформація\n'
            f'- Короткий опис, як працює чекер.\n'
        )
        await message.answer(answer)
    answer = 'Будь ласка, оберіть потрібний розділ ⤵️'
    await Start.free.set()
    await message.answer(
        text=answer,
        reply_markup=reply.kb_start
    )


def register_start(dp: Dispatcher):
    dp.register_message_handler(command_start,
                                CommandStart(),
                                state='*')
