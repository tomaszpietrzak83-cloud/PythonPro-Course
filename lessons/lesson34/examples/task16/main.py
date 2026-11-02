import asyncio
import json
from datetime import datetime, timezone
import aiosqlite
from aiohttp import WSMsgType, web
from demo_support import broadcast, runtime_file

clients = set()
write_lock = asyncio.Lock()


async def database(app):
    db = await aiosqlite.connect(runtime_file("chat.sqlite3"))
    await db.execute(
        "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, nickname TEXT, body TEXT, sent_at TEXT)"
    )
    await db.commit()
    app["db"] = db
    try:
        yield
    finally:
        await db.close()


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    try:
        nickname = (await asyncio.wait_for(ws.receive_str(), 5)).strip()
        if not nickname:
            await ws.close(code=1008)
            return ws
        db = request.app["db"]
        async with write_lock:
            async with db.execute(
                "SELECT nickname, body, sent_at FROM messages ORDER BY id DESC LIMIT 50"
            ) as cursor:
                rows = await cursor.fetchall()
        history = [
            dict(zip(("nickname", "body", "sent_at"), row)) for row in reversed(rows)
        ]
        await ws.send_json({"type": "history", "messages": history})
        clients.add(ws)
        async for message in ws:
            if message.type == WSMsgType.TEXT:
                record = {
                    "nickname": nickname,
                    "body": message.data,
                    "sent_at": datetime.now(timezone.utc).isoformat(),
                }
                async with write_lock:
                    await db.execute(
                        "INSERT INTO messages (nickname, body, sent_at) VALUES (?, ?, ?)",
                        tuple(record.values()),
                    )
                    await db.commit()
                await broadcast(clients, json.dumps({"type": "message", **record}))
    finally:
        clients.discard(ws)
    return ws


def create_app():
    app = web.Application()
    app.cleanup_ctx.append(database)
    app.router.add_get("/ws", chat)
    return app
