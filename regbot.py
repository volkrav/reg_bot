import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import NetworkError

from app.config import Config, load_config
from app.data.db_api import db_create_tables
from app.handlers.back import register_back
from app.handlers.device_list import register_device_list
from app.handlers.device_management import register_device_management
from app.handlers.echo import register_echo
from app.handlers.help import register_help
from app.handlers.registration import register_reg
from app.handlers.start import register_start
from app.middlewares.event_handling import CallbackAnswer, DelMessage

# Configure logging
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# register middleware, filters and handlers,
# the order of the call is fundamental
def register_all_middlewares(dp: Dispatcher, config: Config):
    # dp.setup_middleware(DelMessage())
    dp.setup_middleware(CallbackAnswer())


def register_all_filters(dp: Dispatcher):
    # dp.filters_factory.bind(AdminFilter)
    ...


def register_all_handlers(dp: Dispatcher):
    register_start(dp)
    register_back(dp)
    register_help(dp)
    register_reg(dp)
    register_device_list(dp)
    register_device_management(dp)
    register_echo(dp)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        datefmt='%d-%m-%y %H:%M:%S',
        format=u'%(asctime)s - [%(levelname)s] - (%(name)s).%(funcName)s:%(lineno)d - %(message)s',
        # filename='regbot.log'
    )

    config: Config = await load_config()

    # Initialize bot and dispatcher
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    await db_create_tables()

    # для зручності використання config, щоб отримувати його не через
    # імпорт, а з об'єкту bot. Отримувати таким чином bot.get('config')
    bot['config'] = config

    # Register all func
    register_all_middlewares(dp, config)
    # register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.skip_updates()
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning('reg_bot stopped!')
    except NetworkError:
        logger.error('reg_bot get NetworkError, try restart')
    except Exception as err:
        logger.error(f'reg_bot get {err.args}')
