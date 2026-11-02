from aiohttp import WSMsgType, web


async def echo(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for message in ws:
        if message.type == WSMsgType.TEXT:
            await ws.send_str(f"Server: {message.data}")
    return ws


def create_app():
    app = web.Application()
    app.router.add_get("/ws", echo)
    return app
