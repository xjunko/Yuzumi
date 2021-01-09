from objects.player import Player
from objects import glob

import asyncio, logging

# meme cron to update user stats 
# probably optional idfk

# also based from RealistikDash GD server


# just put cron shit here since its not that much (only 1)

async def update_stats():
    ''' idfk '''
    for player in glob.players.players: 
        await player.update_stats()
    logging.debug('Players Stats is updated!')



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




