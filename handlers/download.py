from aiohttp import web
import os


async def download_apk(request):
    if not os.path.isfile('data/release/latest.apk'):
        return web.Response(text='not yet lol')

    return web.FileResponse('data/release/latest.apk')
