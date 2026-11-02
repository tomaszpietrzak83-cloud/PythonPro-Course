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

    @strawberry.field
    def users(self) -> list[User]:
        return users_db


schema = strawberry.Schema(query=Query)


def create_app():
    app = web.Application()
    app.router.add_route(
        "*", "/graphql", GraphQLView(schema=schema, graphql_ide="graphiql")
    )
    return app
