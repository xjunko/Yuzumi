from aiohttp import web
from enum import IntEnum, unique
from objects import glob

import logging

async def make_response(status:bool = None, *args:list):
    res = ''

    if status == True:
        res += 'SUCCESS\n'
    elif status == False:
        res += 'FAILED\n'

    res += ' '.join([str(x) for x in args])
    return web.Response(text=res)

### DROID
async def normal(s: bool, *res: list):
    return await make_response(s, *res)

async def leaderboard(plays: list):
    args = ['\n'.join(plays)]
    return await make_response(True, *args)

async def login(s: bool, reason: str = None):
    if s == False:
        return await make_response(s, reason)

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

        return await make_response(s, *args)



### NORMAL 
async def text(t: str):
    return web.Response(text=t)

async def json(j: dict):
    return web.json_response(j)
