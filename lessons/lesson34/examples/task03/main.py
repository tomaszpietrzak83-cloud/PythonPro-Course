from aiohttp import WSMsgType, web

clients = set()


async def echo(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    try:
        await ws.send_str(f"You are client number {len(clients)}")
        async for message in ws:
            if message.type == WSMsgType.TEXT:
                await ws.send_str(f"Server: {message.data}")
    finally:
        clients.discard(ws)
    return ws


def create_app():
    app = web.Application()
    app.router.add_get("/ws", echo)
    return app
