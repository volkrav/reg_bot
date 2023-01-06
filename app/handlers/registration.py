import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text

from app.keyboards import reply
from app.misc.classes import CheckIn, Start
from app.handlers.back import command_back, command_start


logger = logging.getLogger(__name__)


async def command_start_registration(message: types.Message, state: FSMContext):
    await message.answer(
        text='✅ В цьому розділі можна зареєструвати новий девайс',
        reply_markup=reply.kb_cancel
    )
    logger.info(
        f'<command_start_registration> OK {message.from_user.id} '
        f'started registration'
    )
    await CheckIn.name.set()
    await message.answer(
        text="Введіть назву девайса ⤵️",
        reply_markup=reply.kb_cancel
    )


async def command_cancel(message: types.Message, state: FSMContext):
    logger.info(
        f'<command_cancel> OK {message.from_user.id} '
        f'canceled registration'
    )
    await state.finish()
    await CheckIn.canceled.set()
    new_state = await state.get_state()
    await command_back(message, state)


async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await CheckIn.ip.set()
    await message.answer(
        text="Введіть IP девайса  ⤵️",
        reply_markup=reply.kb_cancel
    )


async def enter_ip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ip'] = message.text
    await CheckIn.disturb.set()
    await message.answer(
        text='Ввімкнути функцію "Не турбувати вночі:"',
        reply_markup=reply.kb_yes_or_no
    )


async def is_disturb(message: types.Message, state: FSMContext):
    msg_text = (False, True)[message.text == 'Так']
    async with state.proxy() as data:
        data['do_not_disturb'] = msg_text
    async with state.proxy() as data:
        await message.answer(
            f'Я записав наступні дані:\n'
            f'Назва: {data["name"]}\n'
            f'IP: {data["ip"]}\n'
            f'do_not_disturb: {data["do_not_disturb"]}\n'
        )
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
                                state=[CheckIn.name,
                                       CheckIn.ip,
                                       CheckIn.disturb,
                                       ])
    dp.register_message_handler(enter_name,
                                state=CheckIn.name)
    dp.register_message_handler(enter_ip,
                                state=CheckIn.ip)
    dp.register_message_handler(is_disturb,
                                state=CheckIn.disturb)
