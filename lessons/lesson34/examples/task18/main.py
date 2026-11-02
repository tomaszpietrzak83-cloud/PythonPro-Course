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


clients = {"1": set(), "2": set()}


async def notifications(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    user_id = await authenticate(ws)
    if user_id is None:
        return ws
    clients[user_id].add(ws)
    await ws.send_json({"type": "authenticated", "user_id": user_id})
    try:
        async for message in ws:
            if message.type == WSMsgType.TEXT:
                await ws.send_json({"type": "ack"})
    finally:
        clients[user_id].discard(ws)
    return ws


async def create_notification(request):
    claims = None
    try:
        token = request.headers.get("Authorization", "").removeprefix("Bearer ")
        claims = jwt.decode(
            token,
            DEMO_SECRET,
            algorithms=["HS256"],
            options={"require": ["exp", "sub"]},
        )
        if claims["sub"] != "admin":
            raise jwt.InvalidTokenError("Admin required")
    except jwt.InvalidTokenError:
        raise web.HTTPUnauthorized(text="Admin token required")
    try:
        data = await request.json()
        user_id, text = data["user_id"], data["text"]
        if user_id not in clients or not isinstance(text, str) or not text.strip():
            raise ValueError("Invalid notification")
    except (ValueError, TypeError, KeyError):
        raise web.HTTPBadRequest(text="Expected valid user_id and text")
    for connection in tuple(clients[user_id]):
        if not connection.closed:
            try:
                await connection.send_json({"type": "notification", "text": text})
            except (ConnectionError, RuntimeError):
                clients[user_id].discard(connection)
    return web.json_response({"sent_to": user_id}, status=201)


def create_app():
    app = web.Application()
    app.router.add_get("/ws", notifications)
    app.router.add_post("/notifications", create_notification)
    return app
