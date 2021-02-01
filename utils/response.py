from aiohttp import web
from enum import IntEnum, unique
from objects import glob
from pathlib import Path

import logging


### DROID
def make_response(status:bool = None, *args:list):
    res = ''

    if status == True:
        res += 'SUCCESS\n'
    elif status == False:
        res += 'FAILED\n'

    res += ' '.join([str(x) for x in args])
    return web.Response(text=res)


def normal(s: bool, *res: list):
    return make_response(s, *res)

def leaderboard(plays: list):
    args = ['\n'.join(plays)]
    return make_response(True, *args)

def login(s: bool, reason: str = None):
    if s == False:
        return make_response(s, reason)

    elif s == True:
        args = []
        p = reason # shit

        # pain
        args.extend([
            p.id,
            'unk',
            p.stats.rank,
            p.rankBy,
            p.stats.droid_acc,
            p.name,
            f'http://{glob.config.domain}/a/{p.id}'
            ])

        return make_response(s, *args)



### NORMAL 
def Response(d: 'any', **kwargs):
    if 'file' in kwargs:
        d = Path(d)


    if isinstance(d, str):
        return web.Response(text=d)

    elif isinstance(d, (dict, list)):
        return web.json_response(d)

    elif isinstance(d, Path):
        return web.FileResponse(path=d)

    else:
        logging.error("Undefined Response!")
        return web.Response(text=f'Unsupported Response, {str(d)}')

