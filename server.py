from aiohttp import web
from multidict import CIMultiDict
from ffdl import *


async def get(request):
    headers = CIMultiDict()
    uid = get_id(request.query["uid"])
    with cd("data/"):
        book = await create_epub(uid)
        headers["Content-Disposition"] = f'Attachment; filename="{book}"'
        return web.FileResponse(f"data/{book}", headers=headers)


app = web.Application()
app.router.add_get("/get/", get)

web.run_app(app, host="0.0.0.0", port=4444)
