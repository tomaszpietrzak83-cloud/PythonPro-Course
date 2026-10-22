import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

async def hello(request):
    name = request.match_info["name"]
    return web.Response(text=f"Hello, {name}!")

async def main():
    app = web.Application()
    app.router.add_get("/witaj/{name}", hello)
    await demo(app, [
        ('GET', '/witaj/Anna', None, 200),
    ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
