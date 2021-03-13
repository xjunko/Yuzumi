import asyncio
import logging
import oppadc
from pathlib import Path
from enum import Enum, IntEnum, unique

from objects import glob
from objects.beatmap import Beatmap


class droidMods(Enum):
    nm = '-'
    nf = 'n'
    ez = 'e'
    hd = 'h'
    hr = 'r'
    sd = 'u'
    dt = 'd'
    rx = 'x'
    ht = 't'
    nc = 'c'
    fl = 'i'
    v2 = 'v'

    # bullshit mods
    ap = 'p'
    at = 'a'
    pr = 's'
    rez = 'l'
    sc = 'm'
    pf = 'f'
    su = 'b'

@unique
class osuMods(IntEnum):
    nm = 0 << 0
    nf = 1 << 0
    ez = 1 << 1
    td = 1 << 2
    hd = 1 << 3
    hr = 1 << 4
    sd = 1 << 5
    dt = 1 << 6
    rx = 1 << 7
    ht = 1 << 8
    nc = 1 << 9
    fl = 1 << 10
    at = 1 << 11
    so = 1 << 12
    ap = 1 << 13
    pf = 1 << 14
    v2 = 1 << 29



# only used in PPCalculator
def convert_droid(mods: str):
    ''' fucked '''
    modstr = [m.value for m in droidMods]
    val = 4 # hardcode TD to mods
    for n, word in enumerate(mods):
        if word in modstr:
            val += osuMods[droidMods(word).name].value

    return val




class PPCalculator:
    """
     https://github.com/cmyui/gulag/blob/master/utils/recalculator.py
    """
    def __init__(self, path: Path, **kwargs):
            self.bm_path = path

            self.mods = convert_droid(kwargs.get('mods', '-'))
            self.combo = kwargs.get('combo', 0)
            self.nmiss = kwargs.get('nmiss', 0)
            self.acc = kwargs.get('acc', 100.00)

    @classmethod
    async def file_from_osu(cls, md5: str):
        if not (bmap := await Beatmap.from_md5(md5)):
            return logging.error(f"Failed to get map: {md5}")


        return await bmap.download()



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

    scores = await glob.db.fetchall('select * from scores where status = 2')
    for score in scores:
        m = await PPCalculator.from_md5(score['mapHash'])
        if m:
            m.acc = score['acc']
            m.nmiss = score['hitmiss']
            m.combo = score['combo']
            m.mods = convert_droid(score['mods'])

            pp = await m.calc()

            print(score['mapHash'], pp)

            await glob.db.execute("UPDATE scores SET pp = ? where id = ?", [pp, score['id']])



