import logging
import asyncio
import coloredlogs
from quart import Quart

# sus
from objects import glob
from objects.player import Player
from objects.db import sqliteDB

# handlers
from handlers import (cho, api)
from handlers.response import Failed

#
import utils

# testing
from utils import pp
from objects.beatmap import Beatmap

def make_app():
  app = Quart(__name__)
  glob.db = sqliteDB()

  # routes shit idk
  routes = [cho, api]

  for route in routes:
    app.register_blueprint(route, url_prefix=route.prefix)
  return app


app = make_app()

@app.before_serving
async def init_shit():
  # check folder
  utils.check_folder()
  # connect to db
  await glob.db.connect()


  # Testing stuff
  # recalc pp
  # await pp.recalc_scores()
  # test bmap object
  # await Beatmap.from_md5('3ef4d1085a8bee29660a2908cbb1dec9')



  # init players
  player_ids = await glob.db.fetchall("SELECT id FROM users where id != -1")
  for id in player_ids:
    p = await Player.from_sql(id['id']) # maybe do this on login instead?, will prolly take alot of time to start if theres lot of players
    glob.players.add(p)

  async def background_tasks():
    async def update_players_stats():
        for p in glob.players:
          await p.update_stats()

    tasks = [update_players_stats]
    for task in tasks:
      try:
        await task()
      except Exception as err:
        logging.error(f'Failed to complete task: {repr(err)}')

    await asyncio.sleep(glob.config.cron_delay*60)

  # run the background task
  asyncio.ensure_future(background_tasks())

@app.after_serving
async def close_shit():
  await glob.db.close()

@app.errorhandler(500)
async def server_fucked(err):
  return Failed(f'Server Error: {repr(err)}')

@app.route('/')
async def index():
  return {
    'players': len(glob.players),
    'online': len([_ for _ in glob.players if _.online]),
    'title': 'when the impostor is sus'
  }

if __name__ == '__main__':
  coloredlogs.install(level=logging.INFO)
  app.run(port=glob.config.port, use_reloader=False, host=glob.config.host, debug=False)

