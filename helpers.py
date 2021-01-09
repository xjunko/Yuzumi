# stupid shit in here
import os, logging

def checkFolder():
    # checks if data/* folder is missing
    folders = ['replays', 'avatar', 'release']

    if not os.path.isdir('data'):
        os.mkdir('data')

    for folder in folders:
        if not os.path.isdir(f'data/{folder}'):
            logging.info(f'{folder} is missing in data! creating...')
            os.mkdir(f'data/{folder}')


async def readParam(request):
    params = await request.content.read()
    return dict((param.split('=')[0],param.split('=')[-1]) for param in params.decode().split('&'))

class playDataReader:
    def __init__(self, data: str):
        self.data = data

        self.mods = '-'
        self.score = 0
        self.combo = 0
        self.rank = ''
        self.stats = {
                    '300': 0,
                    '100': 0,
                    '50': 0,
                    'miss': 0,
                    'geki': 0,
                    'katsu': 0
                   }
        self.acc = 100
        self.droidAcc = 100
        self.deviceID = None # ???? maybe
        self.isFC = False
        self.username = ''

        self.read()

    def read(self):
        data = self.data.split('+')

        self.mods = data[0]
        self.score = data[1]
        self.combo = data[2]
        self.rank = data[3]

        self.stats['geki'] = data[4]
        self.stats['300'] = data[5]
        self.stats['katsu'] = data[6]
        self.stats['100'] = data[7]
        self.stats['50'] = data[8]
        self.stats['miss'] = data[9]

        self.droidAcc = data[10]
        self.acc = float(self.droidAcc)/1000
        self.deviceID = data[11]
        self.isFC = data[12]
        self.username = data[13]

