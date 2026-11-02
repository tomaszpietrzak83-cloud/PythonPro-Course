import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    author_id: strawberry.Private[str]

    @strawberry.field
    def author(self) -> "User":
        return next(user for user in users_db if user.id == self.author_id)


@strawberry.type
class User:
    id: strawberry.ID
    name: str

    @strawberry.field
    def posts(self) -> list[Post]:
        return [post for post in posts_db if post.author_id == self.id]


users_db = [
    User(id=strawberry.ID("1"), name="Anna"),
    User(id=strawberry.ID("2"), name="Jan"),
]
posts_db = [
    Post(id=strawberry.ID("1"), title="Python", author_id="1"),
    Post(id=strawberry.ID("2"), title="GraphQL", author_id="1"),
    Post(id=strawberry.ID("3"), title="Async", author_id="2"),
]


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return users_db

    @strawberry.field
    def posts(self, author_id: strawberry.ID | None = None) -> list[Post]:
        return [
            post
            for post in posts_db
            if author_id is None or post.author_id == author_id
        ]

    @strawberry.field
    def search_users(self, name: str | None = None) -> list[User]:
        return [
            user
            for user in users_db
            if name is None or name.casefold() in user.name.casefold()
        ]


schema = strawberry.Schema(query=Query)


def create_app():
    app = web.Application()
    app.router.add_route(
        "*", "/graphql", GraphQLView(schema=schema, graphql_ide="graphiql")
    )
    return app
