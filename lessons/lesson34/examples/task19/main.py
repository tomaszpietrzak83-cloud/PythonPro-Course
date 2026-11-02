import strawberry
from aiohttp import WSMsgType, web
from strawberry.aiohttp.views import GraphQLView
from demo_support import broadcast

clients = set()
history_db = []


@strawberry.type
class Profile:
    id: strawberry.ID
    name: str


@strawberry.type
class Message:
    nickname: str
    body: str


@strawberry.type
class Query:
    @strawberry.field
    def history(self) -> list[Message]:
        return history_db

    @strawberry.field
    def profiles(self) -> list[Profile]:
        return [
            Profile(id=strawberry.ID("1"), name="Anna"),
            Profile(id=strawberry.ID("2"), name="Jan"),
        ]


async def chat(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    await ws.send_str("Ready")
    try:
        async for message in ws:
            if message.type == WSMsgType.TEXT:
                record = Message(nickname="Guest", body=message.data)
                history_db.append(record)
                await broadcast(clients, record.body)
    finally:
        clients.discard(ws)
    return ws


schema = strawberry.Schema(query=Query)


def create_app():
    app = web.Application()
    app.router.add_route("*", "/graphql", GraphQLView(schema=schema))
    app.router.add_get("/ws", chat)
    return app
