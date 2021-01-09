from objects.player import Player
import logging

class PlayerList:
    def __init__(self):
        self.players = []

    def __len__(self):
        return len(self.players) - 1 # cuz theres -1 for ???

    def append(self, obj: Player):
        if obj in self.players:
            return logging.debug('?? duplicate obj??')
        
        self.players.append(obj)
        logging.debug(f'added {obj} to playerlist')

    async def get(self, **kwargs):
        for attr in ('name', 'id'):
            if val := kwargs.pop(attr, None):
                break
        else:
            raise ValueError('invalid argument')

        if attr == 'name':
            attr = 'safe_name'
            val = Player.make_safe(val)

        for p in self.players:
            if getattr(p, attr) == val:
                return p

        return self.players[0]

    async def get_login(self, name:str, password:str):
        pass
            