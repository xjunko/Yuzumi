from aiohttp import web
from objects import glob

import helpers
from objects import glob
from utils import response

# post
async def map_leaderboard(request):
    ''' returns leaderboard in o!droid format '''
    params = await helpers.readParam(request)
    args = []
    
    if plays := await glob.db.leaderboard(mapHash=params['hash']):
        for play in plays:

            if play['status'] != 2:
                continue

            p = await glob.players.get(id=int(play['playerID']))
            args.append("{playID} {name} {score} {combo} {rank} {mods} {acc} {gravatarHash}".format(
                playID = play['id'],
                name = p.prefixName,
                score = play['pp'] if glob.config.pp_leaderboard else play['score'],
                combo = play['combo'],
                rank = play['rank'],
                mods = play['mods'] or '-',
                acc = int(play['acc']*1000),
                gravatarHash = f'{p.id}'
            ))

    if args:
        return await response.leaderboard(args)
    else:
        return await response.normal(True)

    


async def view_leaderboard_play(request):
    ''' returns play data '''
    params = await helpers.readParam(request)


    if playData := await glob.db.getPlay(id=int(params["playID"])):
        res = '{mods} {score} {combo} {rank} {hitgeki} {hit300} {hitkatsu} {hit100} {hitmiss} {hit50} {acc}'.format(
            mods = playData['mods'],
            score = playData['score'],
            combo = playData['combo'],
            rank = playData['rank'],
            hitgeki = playData['hitgeki'],
            hit300 = playData['hit300'],
            hitkatsu = playData['hitkatsu'],
            hit100 = playData['hit100'],
            hitmiss = playData['hitmiss'],
            hit50 = playData['hit50'],
            acc = int(playData['acc']*1000)

        )

        return await response.normal(True, res)
    

    return await response.normal(False)


