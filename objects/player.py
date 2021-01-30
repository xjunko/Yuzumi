from dataclasses import dataclass
import logging  #, bcrypt

from objects import glob


@dataclass
class Stats:
    id: int # unused
    rank: int
    tscore: int
    rscore: int
    acc: float
    plays: int
    pp: float
    playing: str = ''
    

    @property
    def droid_acc(self):
        acc = float(self.acc) * 1000
        return str(acc).split('.')[0]


class Player:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.prefix = kwargs.get('prefix', '')
        self.name = kwargs.get('name')
        self.pw_bcrypt = kwargs.get('pswd') # meme not used
        self.safe_name = self.make_safe(self.name) if self.name else None
        self.stats: Stats = None
        self.sign = kwargs.get('sign')

    def __repr__(self):
        return f'<{self.name} - {self.id}>'
        
    @staticmethod
    def make_safe(name):
        return name.lower().replace(' ', '_')

    @property
    def prefixName(self):
        return f'[{self.prefix}]{self.name}' if self.prefix else self.name

    async def fromSQL(self):
        stats = await glob.db.userStats(id=self.id)
        if not stats:
            return logging.error('Failed to get stats')

        self.stats = Stats(**stats)

    """
    async def bcrypt_shit(self):
        ''' retarded function to do retarded stuff, not used atm '''
        password = self.pw_bcrypt # md5 password
        bcrypt_pass = bcrypt.hashpw(password, glob.config.passwd_salt)
        glob.cache['bcrypt'][bcrypt_pass] = password

        self.pw_bcrypt = bcrypt_pass
    """


    async def update_stats(self):
        ''' 
        was originally used for updating rank, rewrite to update stats instead

        '''

        # also credit to miau from oldsu! for this query, might use this but i found a another one that fits my use from gulag
        '''
            SELECT * FROM (SELECT Username, ROW_NUMBER() OVER (ORDER BY RankedScore DESC) AS 'Rank' FROM users) t WHERE Username=@username"
            
            res = await glob.db.fetch(query)

            if res:
                self.stats.rank = res[0]['player_rank']

            await glob.db.execute(f'UPDATE stats SET rank = {self.stats.rank} where id = {self.id}')
        '''

        res = await glob.db.fetchall(
            'select s.acc, s.pp from scores s '
            'where s.playerID = ? and s.status = 2 '
            'order by s.score desc limit 100'
            , [self.id]
            )
        
        if not res:
            return # man

        stats = self.stats

        # avrg acc
        stats.acc = sum([row['acc'] for row in res[:50]]) / min(50, len(res))

        # pp
        #stats.pp = sum([row['pp'] for row in res])
        ## calculate weighted pp based on top 100 scores
        stats.pp = round(sum(row['pp']*0.95 ** i for i, row in enumerate(res)))



        # rank
        rankParam = "pp" if glob.config.pp else "rscore"
        rankBy = stats.pp if glob.config.pp else stats.rscore
        res = await glob.db.fetch(
            'SELECT count(*) AS c FROM stats '
            'WHERE {} > ?'.format(rankParam)
            , [rankBy]
            )

        stats.rank = res[0]['c'] + 1

        # updates stats
        await glob.db.execute('UPDATE stats SET acc = ?, rank = ?, pp = ? WHERE id = ?', [stats.acc, stats.rank, stats.pp, self.id])







    
    async def login(self, password_hash: str):
        bcrypt_cache = glob.cache['bcrypt']
        res = await glob.db.fetch('SELECT id, username, password_hash FROM users where id = ?', [self.id])


        if res:
            res = res[0]
            if password_hash in bcrypt_cache:
                if bcrypt_cache[password_hash] != res['password_hash']:
                    return await response.login(False, 'Wrong username or password')

                return await response.login(True, self)
            else:
                # first login
                if not bcrypt.checkpw(password_hash.encode(), res['password_hash'].encode()):
                    return await response.login(False, 'Wrong username or password')

                bcrypt_cache[password_hash] = res['password_hash']
                return await response.login(True, self)

        return await response.login(False, 'Wrong username or password')



        

        



