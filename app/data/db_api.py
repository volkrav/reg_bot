import logging
from typing import Dict, List

from app.data.DBcm import UseDataBase
from app.misc.classes import Device, create_device
from app.misc.utils import get_now_datetime, get_now_datetime_minus_an_hour
from app.misc.exceptions import ConnectionErrorDB


logger = logging.getLogger(__name__)


async def db_create_tables():
    try:
        async with UseDataBase() as conn:
            with open('app/data/init.sql', 'r') as f:
                sql = f.read()
            await conn.execute(sql)
    except OSError:
        logger.error(
            f'cannot connect to database'
        )
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )


async def db_check_connect() -> bool | ConnectionErrorDB:
    try:
        async with UseDataBase() as conn:
            return True
    except OSError:
        logger.error(
            f'cannot connect to database'
        )
        raise ConnectionErrorDB()


async def db_add_device(device: Device):
    try:
        if not await _check_is_user(device.user_id):
            await _insert('users',
                          {
                              'user_id': device.user_id,
                              'reg_date': await get_now_datetime()
                          })
        await _insert('devices',
                      {
                          'name': device.name,
                          'ip': device.ip,
                          'status': device.status,
                          'do_not_disturb': device.do_not_disturb,
                          'notify': device.notify,
                          'change_date': device.change_date,
                          'user_id': device.user_id,
                          'last_check': await get_now_datetime_minus_an_hour()
                      })
    except ConnectionErrorDB:
        logger.error(
            f'get cannot connect to database'
        )
        raise ConnectionErrorDB()
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )


async def get_all_users_devices(user_id: int) -> List[Device]:
    try:
        async with UseDataBase() as conn:
            device_rows = await conn.fetch(
                '''
                SELECT *
                FROM devices
                WHERE user_id=$1
                ORDER BY id
                ''',
                user_id
            )
        devices_list = [await create_device(device) for device in device_rows]
        return devices_list
    except OSError:
        logger.error(
            f'get cannot connect to database'
        )
        raise ConnectionErrorDB()
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )


async def db_get_device(device_id: int) -> Device:
    try:
        try:
            async with UseDataBase() as conn:
                device_row = await conn.fetchrow(
                    '''
                    SELECT *
                    FROM devices
                    WHERE id=$1
                    ''',
                    int(device_id)
                )
            device = await create_device(device_row)
            return device
        except OSError:
            raise ConnectionErrorDB()
        except:
            return None
    except ConnectionErrorDB:
        logger.error(
            f'get cannot connect to database'
        )
        raise ConnectionErrorDB()
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )


async def db_delete_device(device_id: int) -> None:
    try:
        async with UseDataBase() as conn:
            await conn.execute(
                '''
                DELETE FROM devices
                WHERE id=$1
                ''',
                int(device_id)
            )
        logger.info(
            f'deleted {device_id}'
        )
    except OSError:
        logger.error(
            f'get cannot connect to database'
        )
        raise ConnectionErrorDB()
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )


async def db_update_device(device_id: int, column_newvalues: dict):
    columns = [column for column in column_newvalues.keys()]
    placeholders = [f'${i+1}' for i in range(len(column_newvalues.keys()))]
    set_condition = ', '.join([f'{column}={placeholder}'
                               for column, placeholder in zip(columns, placeholders)])
    new_values = [value for value in column_newvalues.values()]

    try:
        async with UseDataBase() as conn:
            await conn.execute(
                f'UPDATE devices '
                f'SET {set_condition} '
                f'WHERE id=${len(placeholders)+1}',
                *new_values,
                device_id
            )
        logger.info(
            f'update {device_id=}: {columns} on {new_values}'
        )
    except OSError:
        logger.error(
            f'get cannot connect to database'
        )
        raise ConnectionErrorDB()
    except Exception as err:
        logger.error(
            f'get {err.args}'
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
                f'inserting "{values[0]}" into a "{tablename}"'
            )
    except OSError:
        raise ConnectionErrorDB()
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )


async def _check_is_user(user_id: int) -> bool:
    try:
        async with UseDataBase() as conn:
            res = await conn.fetchrow(
                '''
                SELECT * FROM users
                WHERE user_id=$1
                ''',
                user_id,
                record_class=None
            )
        return res != None
    except OSError:
        logger.error(
            f'get cannot connect to database'
        )
        raise ConnectionErrorDB()
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )


async def count_number_of_devices(user_id: int) -> int:
    try:
        print('count_number_of_devices')
        async with UseDataBase() as conn:
            return await conn.fetchval(
                'SELECT count(*) ' +
                'FROM devices ' +
                'WHERE user_id=$1',
                user_id
            )
    except OSError:
        logger.error(
            f'get cannot connect to database'
        )
        raise ConnectionErrorDB()
    except Exception as err:
        logger.error(
            f'get {err.args}'
        )


# async def db_check_is_device(device_id: int) -> bool:
#     async with UseDataBase() as conn:
#         res = await conn.fetchrow(
#             f'SELECT * FROM devices '
#             f'WHERE id=$1',
#             device_id,
#             record_class=None
#         )
#     return res != None
