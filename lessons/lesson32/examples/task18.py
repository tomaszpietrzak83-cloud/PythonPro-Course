import asyncio
from aiohttp import web
from lab_support import launch, span

from aiohttp import ClientSession
from api_support import server, request, object_json

async def chat(request):
    data = await object_json(request)
    prompt = data.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise web.HTTPBadRequest(text="prompt must be non-empty text")
    with span("chat", "Simulated AI wait"):
        await asyncio.sleep(3)
    return web.json_response({"response": f"Received and processed: {prompt}"})

async def status(request):
    return web.json_response({"status": "OK"})

async def main():
    app = web.Application()
    app.router.add_post("/api/v1/chat", chat)
    app.router.add_get("/api/status", status)
    async with server(app) as url:
        async with ClientSession() as client:
            chat_task = asyncio.create_task(request(client, "POST", url + "/api/v1/chat", {"prompt": "Explain await"}))
            await asyncio.sleep(0.1)
            await request(client, "GET", url + "/api/status")
            await chat_task

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
