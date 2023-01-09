import datetime
import logging
from typing import Dict, List, Tuple, Union

from app.data.DBcm import UseDataBase
from app.misc.classes import Device, create_device


logger = logging.getLogger(__name__)


async def db_create_tables():
    async with UseDataBase() as conn:
        with open('app/data/init.sql', 'r') as f:
            sql = f.read()
        await conn.execute(sql)
        print('db_create_tables OK')


async def db_add_device(device: Device):
    if not (await _check_is_user(device.user_id)):
        await _insert('users',
                      {
                          'user_id': device.user_id,
                          'reg_date': datetime.datetime.now()
                      })
    await _insert('devices',
                  {
                      'name': device.name,
                      'ip': device.ip,
                      'status': device.status,
                      'do_not_disturb': device.do_not_disturb,
                      'notify': device.notify,
                      'user_id': device.user_id
                  })


async def get_all_users_devices(user_id: int) -> List[Device]:
    async with UseDataBase() as conn:
        device_rows = await conn.fetch(
            f'SELECT * FROM devices '
            f'WHERE user_id=$1',
            user_id
        )
    devices_list = [await create_device(device) for device in device_rows]
    return devices_list

async def db_get_device(device_id: int) -> Device:
    try:
        async with UseDataBase() as conn:
            device_row = await conn.fetchrow(
                f'SELECT * FROM devices '
                f'WHERE id=$1',
                device_id
            )
            device = await create_device(device_row)
            return device
    except:
        return None


async def db_delete_device(device_id: int) -> None:
    try:
        async with UseDataBase() as conn:
            await conn.execute(
                f'DELETE FROM devices '
                f'WHERE id=$1',
                int(device_id)
            )
        logger.info(
            f'<db_delete_device> OK deleted {device_id}'
        )
    except Exception as err:
        logger.error(
            f'<db_delete_device> BAD get {err.args}'
        )

async def _insert(tablename: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = tuple(column_values.values())
    placeholders = ', '.join(f'${i}' for i in range(
        1, len(column_values.keys())+1))
    try:
        async with UseDataBase() as conn:
            await conn.execute(
                f'INSERT INTO {tablename} '
                f'({columns}) '
                f'VALUES '
                f'({placeholders})',
                *values
            )
            logger.info(
                f'<_insert> OK inserting "{values[0]}" into a "{tablename}"'
            )
    except Exception as err:
        logger.error(
            f'<_insert> BAD when inserting into a {tablename} got an {err}'
        )


async def _check_is_user(user_id: int) -> bool:
    async with UseDataBase() as conn:
        res = await conn.fetchrow(
            f'SELECT * FROM users '
            f'WHERE user_id=$1',
            user_id,
            record_class=None
        )
    return res != None

async def db_check_is_device(device_id: int) -> bool:
    async with UseDataBase() as conn:
        res = await conn.fetchrow(
            f'SELECT * FROM devices '
            f'WHERE id=$1',
            device_id,
            record_class=None
        )
    return res != None
