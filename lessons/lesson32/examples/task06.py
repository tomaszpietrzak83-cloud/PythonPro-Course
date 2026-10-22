import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

import json

async def echo(request):
    try:
        data = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise web.HTTPBadRequest(text="Invalid JSON")
    return web.json_response(data)

async def main():
    app = web.Application()
    app.router.add_post("/api/echo", echo)
    await demo(app, [
        ('POST', '/api/echo', {'message': 'Python'}, 200),
    ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
