import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

async def hello(request):
    return web.Response(text="<h1>Welcome to my page!</h1>", content_type="text/html")

async def main():
    app = web.Application()
    app.router.add_get("/", hello)
    await demo(app, [
        ('GET', '/', None, 200),
    ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
