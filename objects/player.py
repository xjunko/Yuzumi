import logging
import time
from dataclasses import dataclass

from objects import glob
from utils import make_safe


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
    self.name_safe: str = make_safe(self.name) if self.name else None

    self.last_online: float = 0 # soontm
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
    user_data = await glob.db.fetch("SELECT id, prefix, username FROM users WHERE id = ?", [user_id])
    user_stats = await glob.db.fetch("SELECT * FROM stats WHERE id = ?", [user_id])

    p = cls(**user_data[0])
    p.stats = Stats(**user_stats[0])

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






