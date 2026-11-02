from aiohttp import ClientSession


async def send_messages(url):
    replies = []
    async with ClientSession() as session:
        async with session.ws_connect(url) as ws:
            for text in ("Hello", "How are you?", "Goodbye"):
                await ws.send_str(text)
                reply = await ws.receive_str()
                replies.append(reply)
    return replies
