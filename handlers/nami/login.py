from aiohttp import web
from objects import glob

import helpers, logging
from utils import response

# post
async def login(request):
    params = await helpers.readParam(request)
    
    if 'username' not in params or len(params['username']) == 0:
        return response.login(False, 'No username given.')
    
    
    p = await glob.players.get(name=params['username'])

    if not p:
        return response.login(False, 'Player not found.')

    if (res := await p.login(password_hash=params['password'])):
        logging.info(f'{p} is attempting to login!')
        return res

    if res:
        return res # ?????
