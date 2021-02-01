from objects import glob
from utils.response import Response

import json

async def get_stats(request):
    args = request.rel_url.query
    if 'name' not in args and 'id' not in args:
        return Response("Missing parameter, need either name or id.")

    if 'id' in args:
        if not args['id'].isdecimal():
            return Response("Invalid id.")

        pid = args['id']

    elif 'name' in args:
        if len(args['name']) > 16:
            return Response("Invalid name.")

        pid = await glob.db.fetch("SELECT id FROM users where username_safe = ?", [args['name']])

        if not pid:
            return Response("Player not found.")

        pid = pid[0]['id']

    res = await glob.db.fetch("SELECT * FROM stats WHERE id = ?", [pid])

    return Response(res) if res[0] else Response("Player not found.")

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

    

    return Response(players)



