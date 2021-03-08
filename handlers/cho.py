import os
import logging
import copy
import time
from quart import Blueprint, request, send_file

from objects import glob
from objects.player import Player
from objects.score import Score, SubmissionStatus
from handlers.response import Failed, Success, Failure

import utils

bp = Blueprint('cho', __name__)
bp.prefix = '/api/'

## Register / Login
@bp.route('/login.php', methods=['POST'])
async def login():
  params = await request.form

  if 'username' not in params or len(params['username']) == 0:
    return Failed("Invalid username.")

  p = glob.players.get(name=params['username'])

  if not p:
    return Failed("User not found.")

  ## login shites
  ## kinda unsafe cuz its just md5
  ## will add bcrypt (optional maybe)
  res = (await glob.db.fetch("SELECT password_hash, status FROM users WHERE id = ?", [p.id]))[0]
  pswd = res['password_hash']
  status = res['status']

  if params['password'] != pswd:
    return Failed("Wrong password.")

  if status != 0:
    return Failed("Banned.")

  # update last ping
  p.last_online = time.time()

  # make uuid if havent
  if not p.uuid:
    p.uuid = utils.make_uuid(p.name)

  # returns long string of shit
  return Success('{id} {uuid} {rank} {rank_by} {acc} {name} {avatar}'.format(
    id = p.id,
    uuid = p.uuid,
    rank = p.stats.rank,
    rank_by = p.stats.rank_by,
    acc = p.stats.droid_acc,
    name = p.name,
    avatar = f'https://s.gravatar.com/avatar/{p.email_hash}'
  ))


@bp.route('/register.php', methods=['POST'])
async def register():
  params = await request.form

  for args in ['username', 'deviceID', 'email', 'sign']:
    if not params.get(args, None):
      return Failed('Not enough argument.')

  # check username
  if glob.players.get(name=params['username']):
    return Failed("Username already exists.")

  if len(params['username']) < 2:
    return Failed("Username must be longer than 2 characters.")

  player_id = await glob.db.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
  [
    None,
    params['username'],
    utils.make_safe(params['username']),
    params['password'],
    params['deviceID'],
    'NotUsed',
    None,
    None,
    params['email'],
    utils.make_md5(params['email']),
    0
  ])
  # also create stats table
  await glob.db.execute('INSERT INTO stats (id) VALUES (?)', [player_id])

  # create player
  p = await Player.from_sql(player_id)
  glob.players.add(p)

  return Success('Account Created.')


## Leaderboard / View Replay Data / View Actual Replay / Upload Replay
@bp.route('/getrank.php', methods=['POST'])
async def leaderboard():
  params = await request.form

  if 'hash' not in params:
    return Failed('No map hash.')

  res = []
  plays = await glob.db.fetchall("SELECT * FROM scores where mapHash = ? and status = 2 ORDER BY {order_by} DESC".format(order_by='pp' if glob.config.pp_leaderboard else 'score'), [params['hash']])
  for play in plays:
    player = glob.players.get(id=int(play['playerID']))

    res += ['{play_id} {name} {score} {combo} {rank} {mods} {acc} {gravatar_hash}'.format(
      play_id = play['id'],
      name = player.name,
      score = int(play['pp']) if glob.config.pp_leaderboard else play['score'],
      combo = play['combo'],
      rank = play['rank'],
      mods = play['mods'],
      acc = int(play['acc']*1000),
      gravatar_hash = player.email_hash # use gravatar
    )]

  return Success('\n'.join(res))


@bp.route('gettop.php', methods=['POST'])
async def view_score():
  params = await request.form

  play = await glob.db.fetch("SELECT * FROM scores WHERE id = ?", [params['playID']])
  if play:
    play = play[0]
    return Success('{mods} {score} {combo} {rank} {hitgeki} {hit300} {hitkatsu} {hit100} {hitmiss} {hit50} {acc}'.format(
      mods = play['mods'],
      score = int(play['pp']) if glob.config.pp_leaderboard else play['score'],
      combo = play['combo'],
      rank = play['rank'],
      hitgeki = play['hitgeki'],
      hit300 = play['hit300'],
      hitkatsu = play['hitkatsu'],
      hit100 = play['hit100'],
      hitmiss = play['hitmiss'],
      hit50 = play['hit50'],
      acc = int(play['acc']*1000)
    ))

  return Failed('Score not found.')


@bp.route('/upload/<string:replay_path>', methods=['GET'])
async def view_replay(replay_path: str):
  path = f'data/replays/{replay_path}' # already have .odr

  if not os.path.isfile(path):
    return Failed('Replay not found.')

  return await send_file(path)

@bp.route('/upload.php', methods=['POST'])
async def upload_replay():
  replay_id = request.args

  if 'replayID' not in replay_id:
    return Failed('Invalid argument.')

  replay_id = replay_id['replayID']
  path = f'data/replays/{replay_id}.odr' # doesnt have .odr
  raw_replay = (await request.data)[191:][:-48]

  if os.path.isfile(path):
    return Failed('File already exists.')

  with open(path, 'wb') as file:
    file.write(raw_replay)

  return Success('Replay uploaded.')


## Play Submit - god i hate this part

@bp.route('/submit.php', methods=['POST'])
async def submit_play():
  params = await request.form

  if 'userID' not in params:
    return Failed('Not enough argument.')

  p = glob.players.get(id=int(params['userID']))
  p.last_online = time.time()

  if not p:
    return Failed('Player not found, report to server admin.')

  if 'ssid' in params:
    if params['ssid'] != p.uuid:
      return Failed('Mismatch UUID, please relogin.')

  if glob.config.disable_submit:
    return Failed('Score submission is disable right now.')

  if (map_hash := params.get('hash', None)):
    logging.info(f'Changed {p} playing to {map_hash}')
    p.stats.playing = map_hash
    return Success(1, p.id)

  elif (play_data := params.get('data')):
    s = await Score.from_submission(play_data)

    if not s:
      return Failed('Failed to read score data.')

    if s.status == SubmissionStatus.BEST:
      # if this score is better change old play status to 1
      await glob.db.execute('UPDATE scores SET status = 1 WHERE status = 2 AND mapHash = ? AND playerID = ?', [s.mapHash, s.player.id])

    vals = [s.status, s.mapHash, s.player.id, s.score, s.max_combo, s.grade, s.acc, s.h300, s.hgeki, s.h100, s.hkatsu, s.h50, s.hmiss, s.mods, s.pp]

    if s.mapHash == None:
      return Failed('Server cannot find your recent play, maybe it restarted?')

    s.id = await glob.db.execute('INSERT INTO scores VALUES (NULL, ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', vals)

    ### The pain part
    upload_replay = False
    if s.status == SubmissionStatus.BEST:
      upload_replay = True

    ## Update stats
    stats = s.player.stats

    stats.plays += 1
    stats.tscore = s.score

    if s.status == SubmissionStatus.BEST:
      additive = s.score

      if s.prev_best:
        additive -= s.prev_best.score

      stats.rscore += additive

    ## Update Ranked Score stats to db
    await glob.db.execute(
      'UPDATE stats SET rscore = ?, tscore = ?, plays = ? WHERE id = ?',
      [stats.rscore, stats.tscore, stats.plays, s.player.id])

    ## Update stats one more time - i know this is retarded cuz we're already doing it above but im basing it from the old code so
    await s.player.update_stats()

    return Success('{rank} {rank_by} {acc} {map_rank} {score_id}'.format(
      rank = int(stats.rank),
      rank_by = int(stats.rank_by),
      acc = stats.droid_acc,
      map_rank = s.rank,
      score_id = s.id if upload_replay else ""
    ))

  return Failed('Huh?') # Client wasnt supposed to get here.



