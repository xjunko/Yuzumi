import aiosqlite, asyncio
import logging

from objects import glob

class sqliteDB:
    ''' based from cmyui's {pkg: mysql} but sqlite
    '''
    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self):
        self.db = None

    async def checkDatabase(self):
        query = '''
                CREATE TABLE IF NOT EXISTS "maps" ( "hash" TEXT, "data" TEXT, PRIMARY KEY("hash") );

                CREATE TABLE IF NOT EXISTS "scores" (
                  "id" INTEGER,
                  "status" INTEGER,
                  "mapID" INTEGER,
                  "mapHash" TEXT NOT NULL,
                  "playerID" INTEGER NOT NULL,
                  "score" INTEGER NOT NULL,
                  "combo" INTEGER NOT NULL,
                  "rank" TEXT NOT NULL,
                  "acc" INTEGER NOT NULL,
                  "hit300" INTEGER NOT NULL,
                  "hitgeki" INTEGER NOT NULL,
                  "hit100" INTEGER NOT NULL,
                  "hitkatsu" INTEGER NOT NULL,
                  "hit50" INTEGER NOT NULL,
                  "hitmiss" INTEGER NOT NULL,
                  "mods" TEXT,
                  "pp" INTEGER DEFAULT 0,
                  PRIMARY KEY("id" AUTOINCREMENT)
                );

                CREATE TABLE IF NOT EXISTS "stats" (
                  "id" INTEGER,
                  "rank" INTEGER DEFAULT 0,
                  "pp" INTEGER DEFAULT 0,
                  "acc" INTEGER DEFAULT 100.0,
                  "tscore" INTEGER DEFAULT 0,
                  "rscore" INTEGER DEFAULT 0,
                  "plays" INTEGER DEFAULT 0,
                  PRIMARY KEY("id")
                );

                CREATE TABLE IF NOT EXISTS "users" (
                "id"    INTEGER,
                "prefix"    TEXT,
                "username"  TEXT,
                "username_safe" TEXT,
                "password_hash"  TEXT,
                "device_id" TEXT,
                "sign"  TEXT,
                "avatar_id" TEXT,
                "custom_avatar" TEXT,
                "email" TEXT,
                "email_hash"	TEXT,
                "status"    INTEGER DEFAULT 0,
                PRIMARY KEY("id" AUTOINCREMENT)
                );

                INSERT OR IGNORE INTO users (
                id, username, username_safe, password_hash, status
                )
                VALUES(-1, "???", "???", "rembestwaifu69420!!@", -1);

                INSERT OR IGNORE INTO stats (id, rank)
                VALUES (-1, 100);



                '''

        await self.db.executescript(query)

    async def connect(self, filename='stuff.db'):
        self.db = await aiosqlite.connect(filename)
        # self.db.row_factory = aiosqlite.Row # yeah no, i need dict
        self.db.row_factory = self.dict_factory

        logging.debug(f'Database is connected to: {filename}')
        await self.checkDatabase()


    async def close(self):
        logging.debug(f'Database is closed.')
        await self.db.close()


    async def execute(self, query: str, params: list = []):
        async with self.db.execute(query, params) as cursor:
            await self.db.commit()

            lastrowid = cursor.lastrowid

        return lastrowid

    async def fetch(self, query: str, params: list = [], _all: bool = False):
        async with self.db.execute(query, params) as cursor:

            if all:
                res = await cursor.fetchall()
            else:
                res = await cursor.fetchone()

        return res

    async def fetchall(self, query:str, params: list = []):
        return await self.fetch(query, params, _all=True)






