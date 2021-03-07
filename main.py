import logging
import asyncio
import os
from quart import Quart, Response, send_file

# sus
from objects import glob
from objects.player import Player
from objects.db import sqliteDB

# handlers
from handlers import (cho, api)
from handlers.response import Failed

#
import utils

def make_app():
  app = Quart(__name__)
  glob.db = sqliteDB()

  # routes shit idk
  routes = [cho, api]

  for route in routes:
    app.register_blueprint(route, url_prefix=route.prefix)
  return app

logging.basicConfig(level=logging.INFO)
app = make_app()

@app.before_serving
async def init_shit():
  # check folder
  utils.check_folder()

  # connect to db
  await glob.db.connect()

  # init players
  player_ids = await glob.db.fetchall("SELECT id FROM users where id != -1")
  for id in player_ids:
    p = await Player.from_sql(id['id']) # mega sus
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

@app.route('/avatar/<int:player_id>')
async def serve_avatar(player_id: int):

  if not os.path.isfile(f'data/avatars/{player_id}.png'):
    player_id = -1

  return await send_file(f'data/avatars/{player_id}.png')


if __name__ == '__main__':
  app.run(port=80, use_reloader=False, host='0.0.0.0')

