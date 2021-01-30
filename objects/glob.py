from objects import db
from objects.collections import PlayerList

import config

db: 'Database' = db.sqliteDB()
players: PlayerList = PlayerList()


cache = {
    'bcrypt': {}
}