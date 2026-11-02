import asyncio
from aiohttp import WSMsgType, web


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    last_pong = asyncio.get_running_loop().time()

    async def heartbeat():
        while not ws.closed:
            await asyncio.sleep(request.app["interval"])
            if asyncio.get_running_loop().time() - last_pong >= request.app["timeout"]:
                await ws.close(code=1001, message=b"Pong timeout")
                break
            await ws.send_str("ping")

    timer = asyncio.create_task(heartbeat())
    try:
        async for message in ws:
            if message.type == WSMsgType.TEXT and message.data == "pong":
                last_pong = asyncio.get_running_loop().time()
    finally:
        timer.cancel()
        await asyncio.gather(timer, return_exceptions=True)
    return ws


def create_app(interval=30.0, timeout=60.0):
    app = web.Application()
    app["interval"] = interval
    app["timeout"] = timeout
    app.router.add_get("/ws", chat)
    return app
