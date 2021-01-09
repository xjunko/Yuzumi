from aiohttp import web
from objects import glob

import helpers

# post
async def map_leaderboard(request):
    ''' returns leaderboard in o!droid format '''
    params = await helpers.readParam(request)
    
    res = 'SUCCESS'
    if plays := await glob.db.leaderboard(mapHash=params['hash']):
        for play in plays:

            if play['status'] != 2:
                continue

            p = await glob.players.get(id=int(play['playerID']))
            res += "\n{playID} {name} {score} {combo} {rank} {mods} {acc} {gravatarHash}".format(
                playID = play['id'],
                name = p.prefixName,
                score = play['score'],
                combo = play['combo'],
                rank = play['rank'],
                mods = play['mods'] or '-',
                acc = int(play['acc']*1000),
                gravatarHash = f'{p.id}'
            )
    else:
        #res += "\n16 free_#1 420 -420 S - 100000 -69"
        #res += "\n16 what_the_fuck_lol 69 -69 S - 100000 -69"
        #res += "\n16 dont_click_here 69 -69 S - 100000 -69"
        res += '\nBRUH'


    return web.Response(text=res)


async def view_leaderboard_play(request):
    ''' returns play data '''
    params = await helpers.readParam(request)

    res = 'FAILED\nFUCK'

    if playData := await glob.db.getPlay(id=int(params["playID"])):
        res = 'SUCCESS\n{mods} {score} {combo} {rank} {hitgeki} {hit300} {hitkatsu} {hit100} {hitmiss} {hit50} {acc}'.format(
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
    

    return web.Response(text=res)


