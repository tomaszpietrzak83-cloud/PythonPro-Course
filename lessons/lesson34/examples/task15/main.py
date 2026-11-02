import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str


users_db = [
    User(id=strawberry.ID("1"), name="Anna", email="anna@example.com"),
    User(id=strawberry.ID("2"), name="Jan", email="jan@example.com"),
]


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> User | None:
        return next((user for user in users_db if user.id == id), None)


import asyncio
from collections.abc import AsyncGenerator

subscribers = set()
subscription_ready = asyncio.Event()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str) -> User:
        user = User(id=strawberry.ID(str(len(users_db) + 1)), name=name, email=email)
        users_db.append(user)
        for queue in tuple(subscribers):
            queue.put_nowait(user)
        return user


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_registered(self) -> AsyncGenerator[User, None]:
        queue = asyncio.Queue()
        subscribers.add(queue)
        subscription_ready.set()
        try:
            while True:
                yield await queue.get()
        finally:
            subscribers.discard(queue)


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)


def create_app():
    app = web.Application()
    app.router.add_route(
        "*", "/graphql", GraphQLView(schema=schema, graphql_ide="graphiql")
    )
    return app
