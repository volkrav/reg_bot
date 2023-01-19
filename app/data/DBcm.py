import asyncpg
from asyncpg import Connection

from app.config import DbConfig, load_db_config


class UseDataBase:

    async def __aenter__(self) -> Connection:
        db_config: DbConfig = await load_db_config()
        self.conn = await asyncpg.connect(user=db_config.user,
                                          password=db_config.password,
                                          database=db_config.database,
                                          host=db_config.host)
        return self.conn

    async def __aexit__(self, exc_type, exc_value, exc_trace) -> None:
        await self.conn.close()
