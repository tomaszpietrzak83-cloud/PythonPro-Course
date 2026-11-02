from aiohttp import WSMsgType, web
from demo_support import broadcast

rooms = {}


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    room = None
    await ws.send_str("Use /join room-name")
    try:
        async for message in ws:
            if message.type != WSMsgType.TEXT:
                continue
            if message.data.startswith("/join "):
                name = message.data[6:].strip()
                if not name or len(name) > 30:
                    await ws.send_str("Invalid room")
                    continue
                if room is not None:
                    rooms[room].discard(ws)
                    if not rooms[room]:
                        del rooms[room]
                room = name
                rooms.setdefault(room, set()).add(ws)
                await ws.send_str(f"Joined: {room}")
            elif room is not None:
                await broadcast(rooms[room], message.data)
            else:
                await ws.send_str("Join a room first")
    finally:
        if room is not None:
            rooms[room].discard(ws)
            if not rooms[room]:
                del rooms[room]
    return ws


def create_app():
    app = web.Application()
    app.router.add_get("/ws", chat)
    return app
