import asyncio
import os
from contextlib import suppress

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


async def forward(subscription, socket):
    async for event in subscription.listen():
        if event["type"] == "message":
            await socket.send_text(event["data"])


@app.websocket("/ws")
async def chat(socket: WebSocket):
    from redis.asyncio import Redis
    async with Redis.from_url(os.environ["REDIS_URL"], decode_responses=True) as client:
        async with client.pubsub() as subscription:
            await subscription.subscribe("chat")
            await socket.accept()
            listener = asyncio.create_task(forward(subscription, socket))
            try:
                while True:
                    await client.publish("chat", await socket.receive_text())
            except WebSocketDisconnect:
                pass
            finally:
                listener.cancel()
                with suppress(asyncio.CancelledError):
                    await listener


def demo(work):
    class Subscription:
        async def listen(self):
            yield {"type": "subscribe"}
            yield {"type": "message", "data": "Hello"}

    class Socket:
        def __init__(self):
            self.messages = []

        async def send_text(self, message):
            self.messages.append(message)

    async def check():
        sockets = [Socket(), Socket()]
        await asyncio.gather(*(forward(Subscription(), socket) for socket in sockets))
        return [socket.messages for socket in sockets]

    messages = asyncio.run(check())
    assert messages == [["Hello"], ["Hello"]]
    return {"local_channel_fixture": messages}
