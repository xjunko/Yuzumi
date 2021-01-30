from objects import glob
from utils import response

import json

async def get_stats(request):
    args = request.rel_url.query
    if 'name' not in args and 'id' not in args:
        return await response.text("Missing parameter, need either name or id.")

    if 'id' in args:
        if not args['id'].isdecimal():
            return await response.text("Invalid id.")

        pid = args['id']

    elif 'name' in args:
        if len(args['name']) > 16:
            return await response.text("Invalid name.")

        pid = await glob.db.fetch("SELECT id FROM users where username_safe = ?", [args['name']])

        if not pid:
            return await response.text("Player not found.")

        pid = pid[0]['id']

    res = await glob.db.fetch("SELECT * FROM stats WHERE id = ?", [pid])

    return await response.json(res) if res[0] else await response.text("Player not found.")

async def leaderboard(request):
    players = sorted(glob.players.players, key=lambda x: x.stats.rankBy, reverse=True)
    players = {n: {
                    'id': p.id,
                    'name': p.name,
                    'rank': p.stats.rank,
                    'tscore': p.stats.tscore,
                    'rscore': p.stats.rscore,
                    'pp': p.stats.pp
                    }

               for n, p in enumerate(players) if p.id != -1}

    

    return await response.json(players)



