import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


@dataclass
class TgBot:
    token: str


@dataclass
class DbConfig:
    host: str
    database: str
    user: str
    password: str


@dataclass
class Config:
    tg_bot: TgBot
    # db: DbConfig


async def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=os.environ.get('BOT_TOKEN')
        )
    )


async def load_db_config() -> DbConfig:
    return DbConfig(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
    )
