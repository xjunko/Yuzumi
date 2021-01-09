from aiohttp import web
from objects import glob

import pyfiglet

f = pyfiglet.Figlet(font='slant')

# didnt have frontend atm so yea
# prolly wont have frontend cuz fuck frontend
async def index(request):
    res = ''
    res += f.renderText(glob.config.server_name)
    res += """\
                       v  ~.      v
          v           /|
                     / |          v
              v     /__|__
                  \--------/
~~~~~~~~~~~~~~~~~~~`~~~~~~'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Wish you were here?... (I know you do)
"""


    res += f'Players: {len(glob.players)}'    

    return web.Response(text=res)