import time
from aiohttp import WSMsgType, web
from lab_support import event


async def echo(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    started = time.perf_counter()
    try:
        async for message in ws:
            if message.type == WSMsgType.TEXT:
                await ws.send_str(f"Server: {message.data}")
    finally:
        duration = time.perf_counter() - started
        event("metric", "server", "Connection duration", value=duration, unit="s")
    return ws


def create_app():
    app = web.Application()
    app.router.add_get("/ws", echo)
    return app
