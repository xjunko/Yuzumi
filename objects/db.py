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

    async def connect(self, filename='stuff.db'):
        self.db = await aiosqlite.connect(filename)
        # self.db.row_factory = aiosqlite.Row # yeah no, i need dict
        self.db.row_factory = self.dict_factory

        logging.debug(f'Database is connected to: {filename}')


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








    




