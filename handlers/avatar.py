from aiohttp import web
import aiofiles, os


async def view_avatar(request):
    filename_id = request.match_info['avatar_id']

    filename_id = filename_id.split('.')[0] # just incase

    if not os.path.isfile(f'data/avatar/{filename_id}.png'):
        filename_id = -1

    return web.FileResponse(path=f'data/avatar/{filename_id}.png')



