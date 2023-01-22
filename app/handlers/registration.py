import logging

import aiogram.utils.markdown as fmt
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.data.db_api import db_add_device, db_check_connect
from app.handlers.back import command_back, command_start
from app.keyboards import reply
from app.misc.classes import CheckIn, Start, create_device, ConnectionErrorDB
from app.misc.utils import (check_ip, check_name, reply_not_validation_ip,
                            reply_not_validation_name)

logger = logging.getLogger(__name__)


async def command_start_registration(message: types.Message, state: FSMContext):
    await CheckIn.start.set()
    try:
        await db_check_connect()
    except ConnectionErrorDB:
        await message.answer(
            '❌ Вибачте, зараз я не можу обробити цей запит.\n' +
            '✉️ Сповіщення про помилку відправлене адміністратору.\n'
            'Спробуйте повторити запит через деякий час.'
        )
        logger.error(
            f'{message.from_user.id} get ConnectionErrorDB'
        )
        return await command_start(message, state)

    await message.answer(
        text='✅ В цьому розділі можна зареєструвати новий пристрій',
        reply_markup=reply.kb_cancel
    )
    logger.info(
        f'{message.from_user.id} started registration'
    )
    await CheckIn.name.set()
    await message.answer(
        text="Введіть назву пристрою ⤵️",
        reply_markup=reply.kb_cancel
    )


async def command_cancel(message: types.Message, state: FSMContext):
    logger.info(
        f'{message.from_user.id} canceled registration'
    )
    await state.finish()
    await CheckIn.canceled.set()
    await command_back(message, state)


async def enter_name(message: types.Message, state: FSMContext):
    if await check_name(fmt.quote_html(message.text)):
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            data['name'] = fmt.quote_html(message.text)
        logger.info(
            f'{message.from_user.id} '
            f'entered the name {message.text}'
        )
        await CheckIn.ip.set()
        await message.answer(
            text="Введіть IP пристрою  ⤵️",
            reply_markup=reply.kb_cancel
        )
    else:
        logger.warning(
            f'{message.from_user.id} '
            f'entered an unsupported name {message.text}'
        )
        await reply_not_validation_name(message)


async def enter_ip(message: types.Message, state: FSMContext):
    if await check_ip(fmt.quote_html(message.text)):
        async with state.proxy() as data:
            data['ip'] = fmt.quote_html(message.text)
        logger.info(
            f'{message.from_user.id} '
            f'entered the IP {message.text}'
        )
        await CheckIn.do_not_disturb.set()
        await message.answer(
            text='Ввімкнути функцію "Не турбувати вночі"?\n' +
            'Якщо увімкнути цю функцію, то з 23:00 до 7:00 бот ' +
            'не буде надсилати сповіщення про зміну статусу цього пристрою.',
            reply_markup=reply.kb_yes_or_no
        )
    else:
        logger.warning(
            f'{message.from_user.id} '
            f'entered an unsupported IP {message.text}'
        )
        await reply_not_validation_ip(message)


async def is_disturb(message: types.Message, state: FSMContext):
    msg_text = (False, True)[message.text == 'Так']
    async with state.proxy() as data:
        data['do_not_disturb'] = msg_text
    async with state.proxy() as data:
        device = await create_device(data)
    try:
        await db_add_device(device)
        answer = (
            f'✅ Додав до моніторингу новий пристрій:\n'
            f'- <b>Назва:</b> {device.name}\n'
            f'- <b>IP:</b> {device.ip}\n'
            f'- <b>Не турбувати вночі:</b> {("🔴 вимкнено", "🟢 ввімкнено")[device.do_not_disturb]}\n'
        )
    except ConnectionErrorDB:
        answer = (
            f'⚠️ На жаль, при реєстрації пристрою {device.name} виникла помилка.\n'
            f'✉️ Сповіщення про цю помилку відправлене адміністратору.\n'
            f'Спробуйте повторно зареєструвати девайс через деякий час.'
        )
    await message.answer(answer)
    await state.finish()
    await Start.free.set()
    await command_start(message, state)


def register_reg(dp: Dispatcher):
    dp.register_message_handler(command_start_registration,
                                Text(equals='Зареєструвати пристрій',
                                     ignore_case=True),
                                state='*')
    dp.register_message_handler(command_cancel,
                                Text(equals='❌ Скасувати',
                                     ignore_case=True),
                                state=list(CheckIn.all_states_names))
    dp.register_message_handler(enter_name,
                                state=CheckIn.name)
    dp.register_message_handler(enter_ip,
                                state=CheckIn.ip)
    dp.register_message_handler(is_disturb,
                                state=CheckIn.do_not_disturb)
