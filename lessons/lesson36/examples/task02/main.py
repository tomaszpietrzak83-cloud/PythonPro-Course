import asyncio

import psutil
from aiohttp import ClientSession, web


def create_app(memory_percent=lambda: psutil.virtual_memory().percent, threshold=90):
    async def health(request):
        usage = memory_percent()
        healthy = usage < threshold
        return web.json_response(
            {"status": "ok" if healthy else "degraded", "memory_percent": usage},
            status=200 if healthy else 503,
        )
    app = web.Application()
    app.router.add_get("/health", health)
    return app


async def probe():
    samples = iter([40, 95])
    runner = web.AppRunner(create_app(lambda: next(samples)))
    await runner.setup()
    try:
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        host, port = runner.addresses[0]
        results = []
        async with ClientSession() as session:
            for _ in range(2):
                async with session.get(f"http://{host}:{port}/health") as response:
                    results.append({"http": response.status, **await response.json()})
        return results
    finally:
        await runner.cleanup()


def demo(work):
    results = asyncio.run(probe())
    assert [item["http"] for item in results] == [200, 503]
    return {"responses": results}
