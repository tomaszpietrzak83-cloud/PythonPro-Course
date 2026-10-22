import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

from datetime import datetime

async def status(request):
    now = datetime.now().isoformat()
    return web.json_response({"status": "OK", "server_time": now})

async def main():
    app = web.Application()
    app.router.add_get("/api/status", status)
    await demo(app, [
        ('GET', '/api/status', None, 200),
    ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
