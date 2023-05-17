import aiomysql
from aiomysql import DictCursor
import random
import json
import os


class Database:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.pool = None
        self._result = None

    async def _connect(self):
        if self.pool is None or self.pool._closed:
            self.pool = await aiomysql.create_pool(host=self.host, port=self.port, user=self.user,
                                                   password=self.password, db=self.db)

    async def _disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def create_user(self, tg_id):
        await self._connect()
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                json_path = os.path.join(os.path.dirname(__file__), 'defolt_nickname.json')
                with open(json_path) as json_file:
                    data = json.load(json_file)

                await cur.execute("INSERT INTO users (tg_id, state, login) VALUES (%s, %s, %s)",
                                  (tg_id, 'write_nick', data[str(random.randint(0, 99))]))
                await conn.commit()

    async def execute(self, query, *args, **kwargs):
        for _ in range(3):  # Попробуйте выполнить запрос 3 раза перед тем, как прервать его окончательно
            try:
                await self._connect()
                async with self.pool.acquire() as conn:
                    async with conn.cursor(DictCursor) as cur:
                        await cur.execute(query, *args, **kwargs)
                        if query.lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                            await conn.commit()
                        self._result = cur
                        break
            except aiomysql.OperationalError as e:
                if 'Lost connection' in str(e):
                    self.pool = None  # Если соединение потеряно, обнуляем пул
                    continue  # И пытаемся заново
                else:
                    raise  # Если это другая ошибка, просто поднимаем ее дальше

    async def commit(self):
        if self.pool:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await conn.commit()
        else:
            raise ValueError("No connection has been established yet.")

    async def fetchone(self):
        if self._result is not None:
            return await self._result.fetchone()
        else:
            raise ValueError("No query has been executed yet.")

    async def fetchall(self):
        if self._result is not None:
            return await self._result.fetchall()
        else:
            raise ValueError("No query has been executed yet.")

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._disconnect()

    async def get_all_users(self):
        await self.execute("SELECT * FROM users")
        users = await self.fetchall()
        return users
