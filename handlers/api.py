import json
from quart import Blueprint, request, jsonify

from objects import glob

bp = Blueprint('api', __name__)
bp.prefix = '/api/'

@bp.route('/get_online')
async def get_online():
  return {'online': len([_ for _ in glob.players if _.online])}


def get_player(args: list):
  if 'id' not in args and 'name' not in args:
    return 'Need id or name', 400

  if 'id' in args:
    if not args['id'].isdecimal():
      return 'Invalid id', 400

    p = glob.players.get(id=int(args['id']))
  else:
    if len(args['name']) < 2:
      return 'Invalid name', 400

    # get player from name
    p = glob.players.get(name=args['name'])

  return p


@bp.route('/get_user')
async def get_user():
  args = request.args

  p = get_player(args)
  if isinstance(p, tuple):
    return p

  if not p:
    return 'Player not found', 404


  return p.as_json

@bp.route('/get_scores')
async def get_scores():
  params = request.args

  limit = min(params.get('limit', 50), 50)

  p = get_player(params)
  if isinstance(p, tuple):
    return p
    
  if not p:
    return 'Player not found', 404

  scores = await glob.db.fetchall(
  'SELECT id, status, mapHash, score, combo, rank, acc, hit300, hitgeki, '
  'hit100, hitkatsu, hit50, hitmiss, mods, pp FROM scores WHERE playerID = ?'
  'ORDER BY id DESC LIMIT ?'
  , [p.id, limit]
  )

  return jsonify(scores) if scores else {'No score found.'}


