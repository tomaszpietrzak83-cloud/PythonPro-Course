import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView
from strawberry.dataloader import DataLoader
from strawberry.types import Info

users_db = [("1", "Anna"), ("2", "Jan"), ("3", "Alex")]
posts_db = [("1", "Python"), ("2", "GraphQL"), ("3", "Async")]
fetch_count = 0


async def load_posts(keys):
    global fetch_count
    fetch_count += 1
    return [
        [title for author_id, title in posts_db if author_id == key] for key in keys
    ]


@strawberry.type
class User:
    id: strawberry.ID
    name: str

    @strawberry.field
    async def posts(self, info: Info) -> list[str]:
        return await info.context["posts_loader"].load(str(self.id))

    @strawberry.field
    async def naive_posts(self) -> list[str]:
        global fetch_count
        fetch_count += 1
        return [title for author_id, title in posts_db if author_id == self.id]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [User(id=strawberry.ID(id), name=name) for id, name in users_db]


class View(GraphQLView):
    async def get_context(self, request, response):
        return {"request": request, "posts_loader": DataLoader(load_fn=load_posts)}


async def stats(request):
    return web.json_response({"fetch_count": fetch_count})


async def reset(request):
    global fetch_count
    fetch_count = 0
    return web.json_response({"fetch_count": fetch_count})


schema = strawberry.Schema(query=Query)


def create_app():
    app = web.Application()
    app.router.add_route("*", "/graphql", View(schema=schema))
    app.router.add_get("/stats", stats)
    app.router.add_post("/reset", reset)
    return app
