import asyncio
import jwt
from aiohttp import WSMsgType, web

DEMO_SECRET = "public-lesson34-demonstration-secret-only"


async def authenticate(ws):
    try:
        token = await asyncio.wait_for(ws.receive_str(), 5)
        claims = jwt.decode(
            token,
            DEMO_SECRET,
            algorithms=["HS256"],
            options={"require": ["exp", "sub"]},
        )
        if claims["sub"] not in {"1", "2"}:
            raise jwt.InvalidTokenError("Unknown demo user")
        return claims["sub"]
    except (jwt.InvalidTokenError, asyncio.TimeoutError, TypeError):
        await ws.close(code=1008, message=b"Invalid token")
        return None


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    user_id = await authenticate(ws)
    if user_id is None:
        return ws
    await ws.send_json({"type": "authenticated", "user_id": user_id})
    async for message in ws:
        if message.type == WSMsgType.TEXT:
            await ws.send_str(f"Server: {message.data}")
    return ws


def create_app():
    app = web.Application()
    app.router.add_get("/ws", chat)
    return app
