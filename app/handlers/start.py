import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from app.keyboards import reply
from app.misc.classes import Start

logger = logging.getLogger(__name__)


async def command_start(message: types.Message, state: FSMContext):
    logger.info(
        f'{message.from_user.id} started work')
    current_state = await state.get_state()
    if not current_state:
        answer = (
            'Бот для перевірки наявності світла.\n' +
            'Побудований на основі системи моніторингу мережевих пристроїв за допомогою ping.'
        )
        await message.answer(answer)
    answer = 'Будь ласка, оберіть потрібний розділ ⤵️'
    await Start.free.set()
    await message.answer(
        text=answer,
        reply_markup=reply.kb_start
    )


async def get_photo_id(message: types.Message):
    await message.reply(message.photo[-1].file_id)


def register_start(dp: Dispatcher):
    dp.register_message_handler(command_start,
                                CommandStart(),
                                state='*')
    dp.register_message_handler(
        get_photo_id, content_types=types.ContentType.PHOTO, state='*')
