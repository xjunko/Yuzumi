import asyncio
import logging
from aiohttp import web
from aiohttp.abc import AbstractAccessLogger


# fuck my life
from handlers.nami.index import index
from handlers.nami.replay import view_replay, upload_replay
from handlers.nami.login import login
from handlers.nami.leaderboard import view_leaderboard_play, map_leaderboard
from handlers.nami.submit import submit_score
from handlers.nami.register import register

from handlers.avatar import view_avatar
from handlers.download import download_apk

# api
from handlers import api

from cron.cron import cron_loop

#
from objects import glob, score
from objects.player import Player

#
import helpers


def add_routes(app: web.Application):
    ''' meme '''
    app.router.add_get('/', index)

    routes = [
        # cho stuff
        ('/api/upload/{replay_id}', 'GET', view_replay),
        ('/api/upload.php', 'POST', upload_replay),
        ('/api/login.php', 'POST', login),
        ('/api/getrank.php', 'POST', map_leaderboard),
        ('/api/gettop.php', 'POST', view_leaderboard_play),
        ('/api/submit.php', 'POST', submit_score),
        ('/api/register.php', 'POST', register),

        # shit that is not cho stuff
        ('/a/{avatar_id}', 'GET', view_avatar),
        ('/avatar/{avatar_id}', 'GET', view_avatar),
        ('/d/release', 'GET', download_apk),

        # api
        ('/api/get_stats', 'GET', api.get_stats),
        ('/api/leaderboard', 'GET', api.leaderboard)

    ]

    for path, method, handler in routes:
        logging.debug(f'adding {handler.__name__} [{method}]')
        app.router.add_routes([web.route(method, path, handler)])



async def init(loop):
    ''' initiate cock and balls '''
    app = web.Application()
    await glob.db.connect(filename='data.db')

    asyncio.create_task(cache_players())
    asyncio.create_task(cron_loop())


    #await recalc_scores()
    #app.on_startup.append(cache_players)
    app.on_shutdown.append(shutdown)
    return app

async def shutdown(app):
    await glob.db.close()

async def cache_players(app=None):
    players = await glob.db.allPlayer()
    for player in players:
        #if player['id'] == -1:
            #continue


        p = Player(id=int(player['id']), name=player['username'], prefix=player['prefix'], sign=player['sign'])
        await p.fromSQL()
        await p.update_stats()
        glob.players.append(p)

        logging.debug('done caching')


    

class access_log(AbstractAccessLogger):
    def log(self, request, response, time):
        self.logger.info(f'{request.remote} '
                         f'"{request.method}" {request.path}'
                        )


def main():
    logging.basicConfig(level=logging.INFO)

    # do shit
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    add_routes(app)

    # check folders
    helpers.checkFolder()

    try:
        web.run_app(app, port=glob.config.port, host=glob.config.host, access_log_class=access_log)
    except RuntimeError:
        print('...bye')
    except KeyboardInterrupt:
        print('...bye')


if __name__ == "__main__":
    main()