from aiohttp import web
import aiofiles, os

from utils.response import Response


async def view_avatar(request):
    filename_id = request.match_info['avatar_id']

    filename_id = filename_id.split('.')[0] # just incase

    if not os.path.isfile(f'data/avatar/{filename_id}.png'):
        filename_id = -1

    return Response(f'data/avatar/{filename_id}.png', file=True)



