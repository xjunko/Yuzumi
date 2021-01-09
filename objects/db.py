import aiosqlite, asyncio
import logging


class sqlite3Wrapper:
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
                "password"  TEXT,
                "device_id" TEXT,
                "sign"  TEXT,
                "avatar_id" TEXT,
                "custom_avatar" TEXT,
                "email" TEXT,
                "status"    INTEGER DEFAULT 0,
                PRIMARY KEY("id" AUTOINCREMENT)
                );

                INSERT OR IGNORE INTO users (
                id, username, username_safe, password, status
                )
                VALUES(-1, "???", "???", "rembestwaiu69420!!@", -1);

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



    # osu shit starts here
    async def idFromName(self, name: str):
        name = name.lower()
        res = await self.fetch('select id from users where username_safe == ?', [name])
        return res[0]['id'] if res else -1


    async def userStats(self, id: int):
        res = await self.fetch('select * from stats where id = ?', [id])
        return res[0] if res else {}

    async def userInfo(self, id: int):
        res = await self.fetch('select * from users where id = ?', [id])
        return res[0] if res else {}


    async def userData(self, id: int):
        ''' more verbose version of userStats '''
        data = await self.userInfo(id)
        stats = await self.userStats(id)

        if not data or not stats:
            return {}
        else:
            data.update(stats)
            return data

    async def allPlayer(self):
        ''' meme function '''
        return await self.fetch('select * from users')

    async def authUser(self, id:int, password: str):
        ''' bruh moment '''
        if (user := await self.userInfo(id)):
            if password == user['password']:
                return True
        else:
            return False


    # gameplay stuff?
    async def leaderboard(self, mapHash: str):
        res = await self.fetchall('select * from scores where maphash = ? order by score desc', [mapHash])

        return res if res else {}

    async def getPlay(self, id: int):
        res = await self.fetch('select * from scores where id = ?', [id])

        return res[0] if res else {}

    async def userScore(self, id: int, mapHash: str):
        res = await self.fetch('select * from scores where playerID = ? and mapHash = ?', [id, mapHash])
        return res[0] if res else {}








    




