import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

async def search(request):
    query = request.query.get("q")
    if query is None:
        return web.json_response({"error": "Missing q parameter"}, status=400)
    return web.json_response({"search_query": query})

async def main():
    app = web.Application()
    app.router.add_get("/api/search", search)
    await demo(app, [
        ('GET', '/api/search?q=python', None, 200),
        ('GET', '/api/search', None, 400),
    ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
