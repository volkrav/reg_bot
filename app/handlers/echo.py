import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, Text

from app.keyboards import reply


logger = logging.getLogger(__name__)


async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    logger.info(
        f'<send_welcome> sent a message to a {message.from_user.id}')
    await message.reply(
        "Hi!\nI'm EchoBot!\nPowered by aiogram.",
        reply_markup=reply.kb_start)


async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    logger.info(f'<echo> sent a message to a {message.from_user.id}')
    await message.answer(message.text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(send_welcome, CommandStart(), state='*')
    dp.register_message_handler(echo, state='*')
