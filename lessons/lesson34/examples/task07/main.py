from aiohttp import WSMsgType, web
from demo_support import broadcast

clients = set()


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    await ws.send_str("Ready")
    try:
        async for message in ws:
            if message.type == WSMsgType.TEXT:
                await broadcast(clients, message.data)
    finally:
        clients.discard(ws)
    return ws


def create_app():
    app = web.Application()
    app.router.add_get("/ws", chat)
    return app
