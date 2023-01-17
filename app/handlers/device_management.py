import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as fmt

from app.handlers.device_list import command_my_device_list
from app.handlers.echo import echo
from app.keyboards import reply, inline
from app.data.db_api import db_delete_device, db_get_device, db_update_device
from app.misc.classes import DeviceAction, DeviceChange, Device
from app.misc.classes import get_device_view
from app.misc.utils import get_user_id, check_ip, reply_not_validation_ip
from app.misc.utils import check_name, reply_not_validation_name


logger = logging.getLogger(__name__)


async def action_choice(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    action, device_id = callback_data.get('device_id').split('-')
    functions = {
        'change': preparing_to_change_device,
        'del': preparing_to_delete_device,
    }
    current_function = functions.get(action)
    async with state.proxy() as data:
        data['device'] = await db_get_device(device_id)

    await current_function(call.message, state)


async def preparing_to_change_device(message: types.Message, state: FSMContext):
    user_id = await get_user_id(message)
    async with state.proxy() as data:
        device = data.get('device')
    if not device:
        logger.warning(
            f'<change_device> OK {user_id} tried to change a deleted device'
        )
        await message.answer('Цей пристрій був видалений раніше')
        return await command_my_device_list(message, state)
    await DeviceAction.change_device.set()
    async with state.proxy() as data:
        data['device'] = device
    answer = (
        '✏️ Пристрій:\n\n' + await get_device_view(device) +
        '\n\n' +
        'Що будемо змінювати? ⤵️'
    )
    await message.answer(
        text=answer,
        reply_markup=reply.kb_change
    )


async def select_field_to_change(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        device: Device = data.get('device')
    match (message.text, None):
        case 'Назву', _:
            await message.answer(
                f'Поточна назва:\n<b>{device.name}</b>'
            )
            await DeviceChange.name.set()
            await message.answer(
                text="Введіть нову назву пристрою ⤵️",
                reply_markup=reply.kb_cancel
            )
        case 'IP', _:
            await message.answer(
                f'Поточна IP:\n<b>{device.ip}</b>'
            )
            await DeviceChange.ip.set()
            await message.answer(
                text="Введіть нове значення IP пристрою ⤵️",
                reply_markup=reply.kb_cancel
            )
        case 'Не турбувати', _:
            curr_state_disturb = (
                '🟢 ввімкнено' if device.do_not_disturb else '🔴 вимкнено'
            )
            await message.answer(
                f'Поточний стан фунції "Не турбувати вночі": \n'
                f'<b>{curr_state_disturb}</b>')
            await DeviceChange.do_not_disturb.set()
            await message.answer(
                'Виберіть новий стан  ⤵️',
                reply_markup=reply.kb_on_off_cancel
            )
        case 'Сповіщати', _:
            curr_state_notify = (
                '🟢 ввімкнено' if device.notify else '🔴 вимкнено'
            )
            await message.answer(
                f'Поточний стан фунції "Сповіщати": \n'
                f'<b>{curr_state_notify}</b>')
            await DeviceChange.notify.set()
            await message.answer(
                'Виберіть новий стан  ⤵️',
                reply_markup=reply.kb_on_off_cancel
            )
        case _:
            await preparing_to_change_device(message, state)


async def update_device(message: types.Message, state: FSMContext):
    is_check = True
    async with state.proxy() as data:
        device: Device = data.get('device')
    match (await state.get_state(), fmt.quote_html(message.text)):
        case 'DeviceChange:name', new_name:
            if await check_name(new_name):
                await db_update_device(device.id,
                                       {
                                           'name': new_name
                                       }
                                       )
                await message.answer(
                    f'Вдало змінено назву з <b>{device.name}</b> '
                    f'на <b>{new_name}</b>'
                )
                logger.warning(
                    f'<update_device> OK {message.from_user.id} to changed {device.name} on {new_name}'
                )

            else:
                is_check = False
                await reply_not_validation_name(message)
        case 'DeviceChange:ip', new_ip:
            if await check_ip(new_ip):
                await db_update_device(device.id,
                                       {
                                           'ip': new_ip
                                       }
                                       )
                await message.answer(
                    f'Вдало змінено IP з <b>{device.ip}</b> '
                    f'на <b>{new_ip}</b>'
                )
            else:
                is_check = False
                await reply_not_validation_ip(message)
        case 'DeviceChange:do_not_disturb', new_state \
                if new_state in ('🟢 ввімкнено', '🔴 вимкнено'):
            curr_state_do_not_disturb = (
                '🟢 ввімкнено' if device.do_not_disturb else '🔴 вимкнено'
            )
            if curr_state_do_not_disturb != new_state:
                await db_update_device(device.id,
                                       {
                                           'do_not_disturb': not device.do_not_disturb
                                       }
                                       )
                await message.answer(
                    f'Вдало змінено стан фунції "Не турбувати вночі"'
                    f'з <b>{curr_state_do_not_disturb}</b> '
                    f'на <b>{new_state}</b>'
                )
        case 'DeviceChange:notify', new_state \
                if new_state in ('🟢 ввімкнено', '🔴 вимкнено'):
            curr_state_notify = (
                '🟢 ввімкнено' if device.notify else '🔴 вимкнено'
            )
            if curr_state_notify != new_state:
                await db_update_device(device.id,
                                       {
                                           'notify': not device.notify,
                                           'status': 'Не відстежується'
                                       }
                                       )
                await message.answer(
                    f'Вдало змінено стан фунції "Не турбувати вночі" з <b>{curr_state_notify}</b> '
                    f'на <b>{new_state}</b>'
                )
        case _:
            return await echo(message, state)
    if is_check:
        async with state.proxy() as data:
            data['device'] = await db_get_device(device.id)
        await preparing_to_change_device(message, state)


async def preparing_to_delete_device(message: types.Message, state: FSMContext):
    user_id = await get_user_id(message)
    async with state.proxy() as data:
        device = data.get('device')

    if not device:
        logger.warning(
            f'<preparing_to_delete_device> BAD {user_id} tried to change a deleted device'
        )
        await message.answer('Цей пристрій був видалений раніше')
        return await command_my_device_list(message, state)
    try:
        await DeviceAction.del_device.set()
        async with state.proxy() as data:
            data['device'] = device
        answer = (
            '❌  Пристрій:\n\n' + await get_device_view(device) +
            '\n\n' +
            'Видалити? ⤵️'
        )
        await message.answer(
            text=answer,
            reply_markup=reply.kb_yes_or_no,
        )
    except Exception as err:
        logger.error(
            f'<delete_device> {user_id} get {err.args}'
        )
        await command_my_device_list(message, state)


async def answer_yes_or_no(message: types.Message, state: FSMContext):
    match (message.text, await state.get_state()):
        case 'Так', 'DeviceAction:del_device':
            await delete_device(message, state)
        case 'Ні', 'DeviceAction:del_device':
            await command_my_device_list(message, state)


async def delete_device(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        device: Device = data.get('device')

    await db_delete_device(device.id)
    logger.info(
        f'<delete_device> OK {message.from_user.id} deleted {device.name}'
    )
    await message.answer(
        f'Пристрій <b>{device.name}</b> був вдало видалений.'
    )
    await state.finish()
    await command_my_device_list(message, state)


def register_device_management(dp: Dispatcher):
    dp.register_callback_query_handler(action_choice,
                                       inline.cd.filter(),
                                       state='*'
                                       )
    dp.register_message_handler(answer_yes_or_no,
                                Text(equals=['Так', 'Ні'],
                                     ignore_case=True
                                     ),
                                state=['DeviceAction:change_device',
                                       'DeviceAction:del_device']
                                )
    dp.register_message_handler(select_field_to_change,
                                Text(equals=['Назву',
                                             'IP',
                                             'Сповіщати',
                                             'Не турбувати'],
                                     ignore_case=True),
                                state='DeviceAction:change_device'
                                )
    dp.register_message_handler(update_device,
                                state=DeviceChange.all_states)
