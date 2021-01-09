from objects.db import sqlite3Wrapper
from objects.collections import PlayerList

import config

db: sqlite3Wrapper = sqlite3Wrapper()
players: PlayerList = PlayerList()


cache = {
    'bcrypt': {}
}