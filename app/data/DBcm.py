import asyncpg
from asyncpg import Connection

from app.config import load_db_config, DbConfig


# class UseDataBase:

#     async def __aenter__(self) -> Connection:
#         db_config: DbConfig = await load_db_config()
#         self.pool = await asyncpg.create_pool(user=db_config.user,
#                                          password=db_config.password,
#                                          database=db_config.database,
#                                          host=db_config.host
#                                          )
#         self.conn = await self.pool.acquire()
#         # print('Connect DB OK')
#         return self.pool

#     async def __aexit__(self, exc_type, exc_value, exc_trace) -> None:
#         await self.pool.release(self.conn)
#         print('Disconnect DB OK')


class UseDataBase:

    async def __aenter__(self) -> Connection:
        db_config: DbConfig = await load_db_config()
        self.conn = await asyncpg.connect(user=db_config.user,
                                          password=db_config.password,
                                          database=db_config.database,
                                          host=db_config.host)
        print('Connect DB OK')
        return self.conn

    async def __aexit__(self, exc_type, exc_value, exc_trace) -> None:
        await self.conn.close()
        print('Disconnect DB OK')

# from asyncio import AbstractEventLoop
# from typing import Optional

# import asyncpg


# class Database:
#     def __init__(
#         self,
#         name: Optional[str],
#         user: Optional[str],
#         password: Optional[str],
#         host: Optional[str],
#         port: Optional[str],
#         loop: AbstractEventLoop,
#         pool: asyncpg.pool.Pool,
#     ) -> None:
#         self.name = name
#         self.user = user
#         self.password = password
#         self.host = host
#         self.port = port
#         self.loop = loop
#         self.pool = loop.run_until_complete(
#             asyncpg.create_pool(
#                 database=name,
#                 user=user,
#                 password=password,
#                 host=host,
#                 port=port,
#             )
#         )

#     async def create_tables(self) -> None:
#         """create tables in the database."""
#         with open("app/data/init.sql", "r") as f:
#             sql = f.read()
#         await self.pool.execute(sql)

#     async def close_database(self) -> None:
#         await self.pool.close()

#     async def add_user(self, user_id: int, name: str, lang: str) -> None:
#         """add a new user to the database."""
#         await self.pool.execute(f"INSERT INTO Users VALUES({user_id}, '{name}', '{lang}')")
#         logger.info(f"added new user | user_id: {user_id}; name: {name}; language: {lang}")

#     async def verification(self, user_id: int) -> bool:
#         """checks if the user is in the database."""
#         response = await self.pool.fetchrow(f"SELECT EXISTS(SELECT user_id FROM Users WHERE user_id={user_id})")
#         return True if response else False

#     async def get_name(self, user_id: int) -> str:
#         return await self.pool.fetchval(f"SELECT name FROM Users WHERE user_id={user_id}")

#     async def get_lang(self, user_id: int) -> str:
#         return await self.pool.fetchval(f"SELECT lang FROM Users WHERE user_id={user_id}")
