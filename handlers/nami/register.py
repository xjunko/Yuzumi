from aiohttp import web
from objects import glob
from objects.player import Player
from utils import response

import logging
import helpers
import bcrypt

async def register(request):
    params = await helpers.readParam(request)

    name = Player.make_safe(params['username'])
    deviceID = params['deviceID']
    email = params['email']
    sign = params['sign']
    password_hash = params['password']

    # checking
    # name length
    if len(name) > 16:
        return await response.normal(False, 'Name too long.')


    # check device_id
    res = await glob.db.fetch(f'SELECT * FROM users WHERE device_id = ?', [deviceID])
    if res:
        return await response.normal(False, 'Device already registered.')

    # check username
    res = await glob.db.fetch(f'SELECT * FROM users WHERE username_safe = ?', [name])
    if res:
        return await response.normal(False, 'Username already exists.')

    # register fr
    password_bcrypt = bcrypt.hashpw(password_hash.encode(), bcrypt.gensalt()).decode()
    glob.cache['bcrypt'][password_hash] = password_bcrypt

    # insert into users db
    pID = await glob.db.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [
            None,
            params['username'],
            name,
            password_bcrypt,
            deviceID,
            'bruhmoment',
            sign,
            None,
            email,
            0
        ])
    
    # create stats table
    await glob.db.execute('INSERT INTO stats (id) VALUES (?)', [pID])

    p = Player(id=pID, name=params['username'], prefix='', sign=sign)
    await p.fromSQL()
    glob.players.append(p)

    return await response.normal(True, 'Account Created!')


