from aiohttp import web
from objects import glob

import helpers, logging

# post
async def login(request):
    params = await helpers.readParam(request)
    
    if 'username' not in params:
        return web.Response(text='FAILED\what the fuck')
    
    
    p = await glob.players.get(name=params['username'])

    if not p:
        return web.Response(text='FAILED\nwho the fuck are you')

    if res := await p.login(password=params['password']):
        logging.debug(f'{p} is attempting to login!')
        return web.Response(text=res)
    else:
        return web.Response(text='FAILED\nlol wtf wrong password')