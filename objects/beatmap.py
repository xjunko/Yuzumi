import aiohttp
import logging
from enum import IntEnum, unique
from datetime import datetime
from pathlib import Path

from objects import glob

beatmap_folder = Path.cwd() / 'data/beatmaps'

@unique
class RankedStatus(IntEnum):
  Graveyard = -2
  NotSubmitted = -1
  Pending = 0
  Ranked = 1
  Approved = 2
  Qualified = 3
  Loved = 4

  def __str__(self):
    return self.name

class Beatmap:
  def __init__(self, **kwargs):
    self.id: int = kwargs.get('id', -1)
    self.set_id: int = kwargs.get('set_id', -1)
    self.md5: str = kwargs.get('md5', '')

    self.artist: str = kwargs.get('artist', '')
    self.title: str = kwargs.get('title', '')
    self.version: str = kwargs.get('version', '')
    self.creator: str = kwargs.get('creator', '')

    self.last_update: datetime = kwargs.get('last_update', 0.0)
    self.total_length: float = kwargs.get('total_length', 0.0)
    self.max_combo: int = kwargs.get('max_combo', 0)

    self.status: RankedStatus = RankedStatus(kwargs.get('status', -1))

    self.mode: int = kwargs.get('mode', 0)
    self.bpm: float = kwargs.get('bpm', 0.0)
    self.cs: float = kwargs.get('cs', 0.0)
    self.od: float = kwargs.get('od', 0.0)
    self.ar: float = kwargs.get('ar', 0.0)
    self.hp: float = kwargs.get('hp', 0.0)

    self.star: float = kwargs.get('star', 0)


  @property
  def filename(self):
    return f'{self.id}.osu'

  @property
  def full(self):
    return f'{self.artist} - {self.title} [{self.version}]'

  @property
  def gives_reward(self):
    return self.status in (RankedStatus.Ranked, RankedStatus.Approved)

  async def download(self):
    """ Download the map and returns the path """
    path = (beatmap_folder / self.filename)
    if path.exists():
      return path

    url = f'https://old.ppy.sh/osu/{self.id}'
    async with aiohttp.ClientSession() as sess:
      async with sess.get(url) as res:
        if not res or res.status != 200:
          return

        content = await res.read()

    path.write_bytes(content)
    return path

  @classmethod
  async def from_md5(cls, md5: str):
    if bmap := glob.cache['beatmaps'].get(md5):
      return bmap # maybe add timeout like gulag?

    if md5 in glob.cache['unsubmitted']:
      return

    # from sql
    if not (bmap := await cls.from_md5_sql(md5)):
      # Not found in md5, try get from osu!api

      # check api key beforehand
      if len(glob.config.osu_key) < 32:
        logging.info('Failed to get beatmap, invalid api key.')
        return

      if not (bmap := await cls.from_md5_osuapi(md5)):
        return

    # saves to cache
    glob.cache['beatmaps'][md5] = bmap

    return bmap



  @classmethod
  async def from_md5_sql(cls, md5: str):
    if res := await glob.db.fetch(
      'SELECT id, set_id, '
      'artist, title, version, creator, '
      'last_update, total_length, max_combo, '
      'status, '
      'mode, bpm, cs, od, ar, hp, '
      'star '
      'FROM maps WHERE md5 = ?',
      [md5]
    ):
      return cls(**res[0])

  @classmethod
  async def from_md5_osuapi(cls, md5: str):
    url = 'https://old.ppy.sh/api/get_beatmaps'
    params = {'k': glob.config.osu_key, 'h': md5}

    async with aiohttp.ClientSession() as sess:
      async with sess.get(url, params=params) as res:
        if not res or res.status != 200:
          return # fucked up big time

        if not (data := await res.json()):
          return

        bmap = data[0]

    m = cls()
    m.md5 = md5
    m.id = int(bmap['beatmap_id'])
    m.set_id = int(bmap['beatmapset_id'])

    m.artist, m.title, m.version, m.creator = (bmap['artist'], bmap['title'], bmap['version'], bmap['creator'])
    m.last_update = datetime.strptime(bmap['last_update'], '%Y-%m-%d %H:%M:%S')
    m.total_length = float(bmap['total_length'])
    m.max_combo = float(bmap['max_combo'])

    m.status = RankedStatus(int(bmap['approved']))
    m.mode = int(bmap['mode'])
    m.bpm = float(bmap['bpm'])

    m.cs, m.od, m.ar, m.hp = (
      float(bmap['diff_size']), float(bmap['diff_overall']),
      float(bmap['diff_approach']), float(bmap['diff_drain'])
    )

    m.star = float(bmap['difficultyrating'])
    await m.save_to_sql()

    return m


  async def save_to_sql(self):
    await glob.db.execute(
      'REPLACE INTO maps ('
        'md5, id, set_id, '
        'artist, title, version, creator, '
        'last_update, total_length, max_combo, '
        'status, '
        'mode, bpm, cs, od, ar, hp, star'
      ') VALUES ('
        '?, ?, ?, '
        '?, ?, ?, ?,'
        '?, ?, ?, '
        '?, '
        '?, ?, ?, ?, ?, ?, ?)'
      , [
        self.md5, self.id, self.set_id,
        self.artist, self.title, self.version, self.creator,
        self.last_update, self.total_length, self.max_combo,
        self.status,
        self.mode, self.bpm, self.cs, self.od, self.ar, self.hp, self.star
      ]
    )


