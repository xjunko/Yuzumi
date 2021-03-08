import asyncio
import aiofiles
import aiohttp
import json
import logging
import oppadc
from pathlib import Path
from enum import Enum, IntEnum

from objects import glob

beatmap_path = Path.cwd() / 'data/beatmaps'

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
    def __init__(self, path: Path, **kwargs):
            self.bm_path = path

            self.mods = modsBitsFromDroidStr(kwargs.get('mods', '-'))
            self.combo = kwargs.get('combo', 0)
            self.nmiss = kwargs.get('nmiss', 0)
            self.acc = kwargs.get('acc', 100.00)

    @staticmethod
    async def data_from_osuapi(md5: str):
        url = 'https://old.ppy.sh/api/get_beatmaps'

        r = await glob.db.fetch('SELECT data FROM maps WHERE hash = ?', [md5])

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
    async def file_from_osu(cls, md5: str):
        if not (bm_id := await cls.data_from_osuapi(md5)):
            return logging.error(f"Failed to get map data from api md5: {md5}")


        url = f'https://old.ppy.sh/osu/{bm_id}'
        path = beatmap_path / f'{bm_id}.osu'

        if path.exists():
            return path

        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as res:
                if res.status != 200:
                    logging.error(f"Failed to get map {bm_id}")
                    return None

                content = await res.read()

        path.write_bytes(content)
        return path




    @classmethod
    async def from_md5(cls, md5: str, **kwargs):
        if not glob.config.pp or not (res := await cls.file_from_osu(md5)):
            return False

        return cls(res, **kwargs)



    async def calc(self):
        curMap = oppadc.OsuMap(file_path=self.bm_path)
        pp = curMap.getPP(self.mods, accuracy=self.acc, misses=self.nmiss, combo=self.combo)

        return pp.total_pp


async def recalc_scores():
    ''' never use this unless something fucked up/testing '''
    print('recalculatin sk0r3')

    scores = await glob.db.fetchall('select * from scores where status = 2 and pp = 0')
    for score in scores:
        m = await PPCalculator.from_md5(score['mapHash'])
        if m:
            m.acc = score['acc']
            m.nmiss = score['hitmiss']
            m.combo = score['combo']
            m.mods = modsBitsFromDroidStr(score['mods'])

            pp = await m.calc()

            print(score['mapHash'], pp)

            await glob.db.execute("UPDATE scores SET pp = ? where id = ?", [pp, score['id']])



