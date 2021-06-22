import config
from .collections import PlayerList

players: PlayerList = PlayerList()

cache: dict = {
  'hashes': {},
  'beatmaps': {},
  'unsubmitted': {}
}
