import asyncio
from aiohttp import WSMsgType, web
from demo_support import broadcast

clients = set()


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    try:
        nickname = (await asyncio.wait_for(ws.receive_str(), 5)).strip()
        if not nickname or len(nickname) > 20:
            await ws.close(code=1008, message=b"Invalid nickname")
            return ws
        clients.add(ws)
        await ws.send_str(f"Ready: {nickname}")
        async for message in ws:
            if message.type == WSMsgType.TEXT:
                await broadcast(clients, f"{nickname}: {message.data}")
    finally:
        clients.discard(ws)
    return ws


def create_app():
    app = web.Application()
    app.router.add_get("/ws", chat)
    return app
