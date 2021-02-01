import aiofiles, os

from utils import response

# get
async def view_replay(request):
    replay_id = request.match_info['replay_id']

    if not os.path.isfile(f'data/replays/{replay_id}'):
        return response.normal(False, 'Replay not found.')
    
    return response.Response(f'data/replays/{replay_id}', file=True)


# post
# TODO: add verification stuff maybe? so ppl cant just upload shit here
async def upload_replay(request):
    replay_id = request.rel_url.query['replayID']
    body = await request.content.read()
    replay = body[191:][:-48] # 

    if os.path.isfile(f'data/replays/{replay_id}.odr'):
        # if file odi exist we just return 
        return response.normal(True, 'Already uploaded.')

    # if shit is fayn then just save the file
    async with aiofiles.open(f'data/replays/{replay_id}.odr', 'wb') as file:
        await file.write(replay)

    return response.normal(True, 'Uploaded!')



