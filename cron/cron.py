from objects.player import Player
from objects import glob

import asyncio, logging

# meme cron to update ranks
# probably optional idfk

# also "kinda" inspired from RealistikDash GD server


# just put cron shit here since its not that much (only 1)

async def update_stats():
    ''' idfk '''
    # loo00p
    for player in glob.players.players: # doesnt work on init, since cache_player call the thing
        await player.update_stats() # lol
    logging.debug('ooo yeaa bitch we updated thh33 rankkk')



tasks = [update_stats]

async def cron_run():
    for task in tasks:
        try:
            await task()
        except Exception as err:
            logging.error(f'shit fuck {err}')


async def cron_loop():
    delay = glob.config.cron_delay * 60 # minutes
    while True:
        await cron_run()
        logging.debug('yea we cron-ing')
        await asyncio.sleep(delay)




