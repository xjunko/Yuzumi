from aiohttp import web
from objects import glob
from objects.player import Player

import logging
import helpers

async def register(request):
    params = await helpers.readParam(request)

    name = Player.make_safe(params['username'])
    deviceID = params['deviceID']
    email = params['email']
    sign = params['sign']

    # checking
    # check device_id
    res = await glob.db.fetch(f'select * from users where device_id = ?', [deviceID])
    if res:
        return web.Response(text='FAILED\nDevice already registered.')

    # check username
    res = await glob.db.fetch(f'select * from users where username_safe = ?', [name])
    if res:
        return web.Response(text='FAILED\nUsername already exist.')

    # register fr
    pID = await glob.db.execute('insert into users values (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [
            None,
            params['username'],
            name,
            params['password'],
            deviceID,
            'bruhmoment',
            sign,
            None,
            email,
            0
        ])
    
    # create stats table
    await glob.db.execute('insert into stats (id) values (?)', [pID])

    p = Player(id=pID, name=params['username'], prefix='', sign=sign)
    await p.fromSQL()
    glob.players.append(p)

    return web.Response(text='SUCCESS\nACCOUNT CREATED')


