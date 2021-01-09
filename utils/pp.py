"""

    This shit is cursed, use on your own accord.

"""


import asyncio
import aiofiles
import aiohttp
import json
#from pathlib import Path
from enum import Enum, IntEnum

from objects import glob

#beatmap_path = Path.cwd() / 'data/'

class droidMods(Enum):
    nm = '-'
    ez = 'e'
    nf = 'f'
    hr = 'r'
    hd = 'h'
    fl = 'i'
    dt = 'd'
    nc = 'c'
    ht = 't'
    v2 = 'v'

class osuMods(IntEnum):
    nm = 0 << 0
    nf = 1 << 0
    ez = 1 << 1
    hd = 1 << 3
    hr = 1 << 4
    dt = 1 << 6
    ht = 1 << 8
    nc = 1 << 9
    fl = 1 << 10
    v2 = 1 << 29



# only used in PPCalculator
def modsBitsFromDroidStr(mods: str):
    ''' fucked '''
    modstr = [m.value for m in droidMods]
    val = 4 # hardcode TD to mods
    for n, word in enumerate(mods):
        if word in modstr:
            val += osuMods[droidMods(word).name].value

    return val




class PPCalculator:
    """ https://github.com/cmyui/gulag/blob/master/utils/recalculator.py

    
        also it uses cpol's pp api so thats fucking retarded

        TODO:
        local pp calculation

    """
    def __init__(self, map_id:int, **kwargs):
            self.map_id  = map_id

            self.mods = modsBitsFromDroidStr(kwargs.get('mods', '-'))
            self.combo = kwargs.get('combo', 0)
            self.nmiss = kwargs.get('nmiss', 0)
            self.acc = kwargs.get('acc', 100.00)

    @staticmethod
    async def data_from_osuapi(md5: str):
        url = 'https://old.ppy.sh/api/get_beatmaps'

        r = await glob.db.fetch('select data from maps where hash = ?', [md5])

        if r:
            return json.loads(r[0]['data'])['beatmap_id']

        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, params={'k': glob.config.osu_key, 'h': md5}) as res:
                if res and res.status == 200:
                    try:
                        data = (await res.json())[0]
                    except:
                        return None

                    # save shit into db
                    await glob.db.execute('INSERT or IGNORE into maps values(?, ?)', [str(md5), json.dumps(data, indent=4)])

                    return data['beatmap_id']




    @classmethod
    async def from_md5(cls, md5: str, **kwargs):
        if not (res := await cls.data_from_osuapi(md5)):
            return 0

        # return 0 if pp system is disabled
        if not glob.config.pp:
            return 0

        return cls(res, **kwargs)



    async def calc(self):
        ''' call cyperdark api for pp, will rewrite to use .osu file instead '''
        params = {}
        params['id'] = self.map_id

        if self.mods:
            params['mods'] = int(self.mods)
        if self.combo:
            params['combo'] = int(self.combo)
        if self.nmiss:
            params['miss'] = int(self.nmiss)
        if self.acc:
            params['acc'] = int(self.acc)



        url = 'https://pp.osuck.net/pp'

        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, params=params) as res:
                if res and res.status == 200:
                    data = await res.json()
                    return data['pp']['current']

        return 0.0




async def recalc_scores():
    ''' never use this unless something fucked up/testing '''
    print('recalculatin sk0r3')

    #scores = await glob.db.fetchall('select * from scores where pp = 0')
    scores = await glob.db.fetchall('select * from scores where status = 2')
    for score in scores:
        m = await PPCalculator.from_md5(score['mapHash'])

        if m:
            m.acc = score['acc']
            m.nmiss = score['hitmiss']
            m.combo = score['combo']
            mods = droidMods(score['mods'])
            m.mods = osuMods[mods.name].value

            pp = await m.calc()

            await glob.db.execute('update scores set pp = ? where id = ?', [pp, score['id']])
            print(f'finished calculating {score["id"]} => pp: {pp}')
        else:
            print(f'failed calculating {score["id"]}')
