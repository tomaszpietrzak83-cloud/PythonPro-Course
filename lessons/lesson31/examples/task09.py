import asyncio
import aiohttp
from aiohttp import web
from lab_support import event, launch, metric, span

async def respond(request):
    await asyncio.sleep(0.2)
    return web.Response(status=int(request.match_info["status"]))

async def fetch_status(session, url):
    with span(url.rsplit("/", 1)[-1], "HTTP"):
        try:
            async with session.get(url) as response:
                event("log", "HTTP", f"{url} -> {response.status}")
                return response.status
        except (aiohttp.ClientError, asyncio.TimeoutError) as error:
            event("log", "HTTP", str(error))
            return None

async def main():
    application = web.Application()
    application.router.add_get("/{status}", respond)
    runner = web.AppRunner(application)
    await runner.setup()
    try:
        server = await asyncio.get_running_loop().create_server(
            runner.server, "127.0.0.1", 0
        )
        async with server:
            port = server.sockets[0].getsockname()[1]
            urls = [f"http://127.0.0.1:{port}/{s}" for s in (200, 404, 503)]
            timeout = aiohttp.ClientTimeout(total=3)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                statuses = await asyncio.gather(
                    *(fetch_status(session, url) for url in urls)
                )
            metric("HTTP statuses", str(statuses))
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
