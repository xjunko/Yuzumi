import logging
import time
import hashlib
from dataclasses import dataclass

from objects import glob
import utils


@dataclass
class Stats:
  id: int
  rank: int
  tscore: int
  rscore: int
  acc: float
  plays: int
  pp: float
  playing: str = None

  @property
  def droid_acc(self):
    return int(self.acc*1000)

  @property
  def droid_submit_stats(self):
    # returns current stats
    return f'{self.rank} {self.rank_by} {self.droid_acc} 0'

  @property
  def rank_by(self):
    return self.pp if glob.config.pp else self.rscore

  @property
  def as_json(self):
    return {
      'id': self.id,
      'rank': self.rank,
      'total_score': self.tscore,
      'ranked_score': self.rscore,
      'accurancy': self.acc,
      'plays': self.plays,
      'pp': self.pp,
      'is_playing': self.playing

    }


class Player:
  def __init__(self, **kwargs):
    self.id: str = kwargs.get('id')
    self.prefix: str = kwargs.get('prefix', '')
    self.name: str = kwargs.get('username')
    self.name_safe: str = utils.make_safe(self.name) if self.name else None

    #
    self.email_hash: str = kwargs.get('email_hash', '35da3c1a5130111d0e3a5f353389b476') # used for gravatar, default to my pfp lole
    self.uuid: str = kwargs.get('uuid', None) # ...yea


    self.last_online: float = 0
    self.stats: Stats = None

  def __repr__(self):
    return f'<{self.id} - {self.name}>'

  @property
  def online(self):
    # 30 seconds timeout, not really accurate cuz we update the last_online time on login and submit
    return time.time()-30 < self.last_online


  @property
  def as_json(self):
    return {
      'id': self.id,
      'prefix': self.prefix,
      'name': self.name,
      'online': self.online,
      'stats': self.stats.as_json
    }

  @classmethod
  async def from_sql(cls, user_id: int):
    user_data = await glob.db.fetch("SELECT id, prefix, username, email_hash, email FROM users WHERE id = ?", [user_id])
    user_stats = await glob.db.fetch("SELECT * FROM stats WHERE id = ?", [user_id])

    if not user_data or not user_stats:
      raise Exception('Failed to get user from database.')

    user_data = user_data[0]
    user_stats = user_stats[0]

    # fix email_hash if its none and user got email (there should be)
    if user_data['email_hash'] == None and user_data['email'] != None:
      email_hash = utils.make_md5(user_data['email'])
      await glob.db.execute('UPDATE users SET email_hash = ? WHERE id = ?', [email_hash, user_id])

    user_data.pop('email', None)

    p = cls(**user_data)
    p.stats = Stats(**user_stats)

    return p


  async def update_stats(self):
    res = await glob.db.fetchall(
      'SELECT s.acc, s.pp FROM scores s '
      'WHERE s.playerID = ? and s.status = 2 '
      'ORDER BY s.score DESC LIMIT 100'
      , [self.id]
    )

    if not res:
      return #logging.error(f'Failed to find player scores when updating stats. (Ignore if the player is new, id: {self.id})')

    stats = self.stats

    # average acc
    stats.acc = sum([row['acc'] for row in res[:50]]) / min(50, len(res))

    # pp
    ## weight and shit
    stats.pp = round(sum(row['pp']*0.95 ** i for i, row in enumerate(res)))

    # rank
    rank_by = 'pp' if glob.config.pp else 'rscore'
    higher_by = stats.pp if glob.config.pp else stats.rscore
    res = await glob.db.fetch(
      'SELECT count(*) AS c FROM stats '
      'WHERE {} > ?'.format(rank_by)
      , [higher_by]
    )


    stats.rank = res[0]['c'] + 1

    # update into db
    await glob.db.execute('UPDATE stats SET acc = ?, rank = ?, pp = ? WHERE id = ?', [stats.acc, stats.rank, stats.pp, self.id])






