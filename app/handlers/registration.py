import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text

from app.keyboards import reply
from app.misc.classes import CheckIn, Start
from app.misc.classes import create_device
from app.handlers.back import command_back, command_start
from app.data.db_api import db_add_device
from app.misc.utils import check_ip


logger = logging.getLogger(__name__)


async def command_start_registration(message: types.Message, state: FSMContext):
    await message.answer(
        text='✅ В цьому розділі можна зареєструвати новий пристрій',
        reply_markup=reply.kb_cancel
    )
    logger.info(
        f'<command_start_registration> OK {message.from_user.id} '
        f'started registration'
    )
    await CheckIn.name.set()
    await message.answer(
        text="Введіть назву пристрою ⤵️",
        reply_markup=reply.kb_cancel
    )


async def command_cancel(message: types.Message, state: FSMContext):
    logger.info(
        f'<command_cancel> OK {message.from_user.id} '
        f'canceled registration'
    )
    await state.finish()
    await CheckIn.canceled.set()
    await command_back(message, state)


async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['name'] = message.text
    await CheckIn.ip.set()
    await message.answer(
        text="Введіть IP пристрою  ⤵️",
        reply_markup=reply.kb_cancel
    )


async def enter_ip(message: types.Message, state: FSMContext):
    if await check_ip(message.text):
        async with state.proxy() as data:
            data['ip'] = message.text
        await CheckIn.do_not_disturb.set()
        await message.answer(
            text='Ввімкнути функцію "Не турбувати вночі:"',
            reply_markup=reply.kb_yes_or_no
        )
    else:
        await message.reply(
            text='‼️ Невірний формат IP адреси ‼️\n\n' +
            'IP-адреси є набір з чотирьох чисел, розділених точками, ' +
            'наприклад, 192.158.1.38. Кожне число цього набору належить ' +
            'інтервалу від 0 до 255. Таким чином, повний діапазон ' +
            'IP-адресації – це адреси від 0.0.0.0 до 255.255.255.255\n\n' +
            'Введіть, будь ласка, коректне значення IP пристрою  ⤵️',
            reply_markup=reply.btn_cancel
        )


async def is_disturb(message: types.Message, state: FSMContext):
    msg_text = (False, True)[message.text == 'Так']
    async with state.proxy() as data:
        data['do_not_disturb'] = msg_text
    async with state.proxy() as data:
        device = await create_device(data)
    try:
        await db_add_device(device)
        # do_not_disturb = ('🔴', '🟢')[device.do_not_disturb]
        answer = (
            f'✅ Додав до моніторингу новий пристрій:\n'
            f'- <b>Назва:</b> {device.name}\n'
            f'- <b>IP:</b> {device.ip}\n'
            f'- <b>Не турбувати вночі:</b> {("🔴", "🟢")[device.do_not_disturb]}\n'
        )
    except Exception as err:
        answer = (
            f'⚠️ На жаль, при реєстрації пристрою {device.name} виникла помилка.\n'
            f'✉️ Сповіщення про помилку відправлене адміністратору.\n'
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
