"""Actual HTTP cases, expected outcomes and evidence for all twenty exercises."""


def case(method, path, data=None, status=200, expected=None, headers=None):
    return dict(
        method=method,
        path=path,
        data=data,
        status=status,
        expected=expected,
        headers=headers or {},
    )


BOOK = {"title": "Python Basics", "price": 2500}
ANNA = {"X-API-Key": "demo-anna-key"}
JAN = {"X-API-Key": "demo-jan-key"}
POST = {
    "title": "Learning Python",
    "body": "Python is great. Async APIs help us build responsive services and learn clear architecture.",
}


def scenarios(n):
    if n == 1:
        return [
            case("GET", "/", expected={"message": "Hello"}),
            case("GET", "/time"),
            case("GET", "/random"),
        ]
    if n == 2:
        return [
            case("GET", "/greet/Anna", expected={"message": "Hello, Anna!"}),
            case("GET", "/greet/A", status=422),
        ]
    if n == 3:
        return [
            case(
                "GET",
                f"/calculate?a=12&b=3&operation={op}",
                expected={"result": result},
            )
            for op, result in [
                ("add", 15),
                ("subtract", 9),
                ("multiply", 36),
                ("divide", 4),
            ]
        ] + [
            case("GET", "/calculate?a=1&b=0&operation=divide", status=400),
            case("GET", "/calculate?a=text&b=1", status=422),
        ]
    if n == 4:
        return [
            case(
                "POST",
                "/products",
                {"name": "Book", "price": 12.5, "quantity": 3},
                expected={"total_price": 37.5},
            ),
            case(
                "POST",
                "/products",
                {"name": "Book", "price": -1, "quantity": 1},
                status=422,
            ),
        ]
    if n in (5, 6, 9, 13, 15, 18):
        create_status = 200 if n == 5 else 201
        result = [
            case(
                "POST",
                "/books",
                BOOK,
                status=create_status,
                expected={"id": 1, **BOOK},
            ),
            case("GET", "/books"),
            case("GET", "/books/1", expected={"title": "Python Basics"}),
        ]
        if n == 9:
            result.append(
                case("GET", "/authors", expected=[{"id": 1, "name": "Anna"}])
            )
        if n in (13, 18):
            result.append(
                case(
                    "PUT",
                    "/books/1",
                    {"title": "Advanced Python", "price": 3000},
                    expected={"title": "Advanced Python"},
                )
            )
        if n == 18:
            result.extend([
                case(
                    "POST",
                    "/books",
                    {
                        "title": "Async Patterns",
                        "price": 1500,
                        "category": "Technology",
                    },
                    status=201,
                ),
                case(
                    "GET",
                    "/books?category=Technology&min_price=1000&max_price=2000&sort_by=title&skip=0&limit=1",
                    expected=[
                        {
                            "id": 2,
                            "title": "Async Patterns",
                            "price": 1500,
                            "category": "Technology",
                        }
                    ],
                ),
                case("GET", "/books?skip=-1", status=422),
                case("GET", "/books?sort_by=unknown", status=400),
            ])
        result.extend([
            case("DELETE", "/books/1", status=200 if n == 5 else 204),
            case("GET", "/books/1", status=404),
        ])
        return result
    if n == 7:
        return [
            case(
                "POST",
                "/users",
                {"email": "anna@example.com"},
                expected={"email": "anna@example.com"},
            ),
            case("POST", "/users", {"email": "not-an-email"}, status=422),
        ]
    if n == 8:
        return [
            case("GET", "/openapi.json"),
            case("GET", "/docs"),
            case(
                "POST",
                "/books",
                {"title": "Python Basics"},
                expected={"title": "Python Basics"},
            ),
        ]
    if n == 10:
        return [
            case("GET", "/books", status=401),
            *[
                case("GET", path, headers={"X-API-Key": "lesson-demo-key"})
                for path in ("/books", "/authors", "/stats")
            ],
            case("GET", "/stats", status=401, headers={"X-API-Key": "wrong"}),
        ]
    if n == 11:
        return [
            case(
                "POST",
                "/books",
                {
                    "title": "Python",
                    "author": {"name": "Anna", "email": "anna@example.com"},
                    "price": 20,
                },
            ),
            case(
                "POST",
                "/books",
                {
                    "title": "Python",
                    "author": {"name": "Anna", "email": "broken"},
                    "price": 20,
                },
                status=422,
            ),
        ]
    if n == 12:
        return [
            case(
                "POST",
                "/products",
                {"name": "Book123", "price": 40, "category": "Books"},
            ),
            case(
                "POST",
                "/products",
                {"name": "bad name!", "price": 40, "category": "Books"},
                status=422,
            ),
            case(
                "POST",
                "/products",
                {"name": "Book", "price": 10001, "category": "Books"},
                status=422,
            ),
            case(
                "POST",
                "/products",
                {"name": "Book", "price": 40, "category": "Other"},
                status=422,
            ),
        ]
    if n == 14:
        return [
            case("POST", "/authors", {"name": "Anna"}, status=201),
            case(
                "POST",
                "/books",
                {"title": "Python Basics", "author_id": 1},
                status=201,
            ),
            case(
                "POST",
                "/books",
                {"title": "Async Patterns", "author_id": 1},
                status=201,
            ),
            case(
                "GET",
                "/authors/1/books",
                expected=[
                    {"id": 1, "title": "Python Basics"},
                    {"id": 2, "title": "Async Patterns"},
                ],
            ),
            case("GET", "/authors/99/books", status=404),
        ]
    if n == 16:
        return [case("GET", "/books"), case("GET", "/missing", status=404)]
    if n == 17:
        return [
            case("GET", "/cache", expected={"source": "startup-file"}),
            case(
                "PUT",
                "/cache/topic?value=FastAPI",
                expected={"topic": "FastAPI"},
            ),
            case("GET", "/cache", expected={"topic": "FastAPI"}),
        ]
    if n in (19, 20):
        result = [
            case("POST", "/users", {"name": "Anna"}, status=201),
            case("POST", "/users", {"name": "Jan"}, status=201),
            case("POST", "/users", {"name": "Anna"}, status=409),
            case(
                "GET",
                "/users",
                expected=[{"id": 1, "name": "Anna"}, {"id": 2, "name": "Jan"}],
            ),
            case("GET", "/users/1"),
            case("POST", "/posts", POST, status=201, headers=ANNA),
            case("GET", "/posts"),
            case("GET", "/posts/1"),
            case(
                "PUT",
                "/posts/1",
                {**POST, "title": "Unauthorized edit"},
                status=403,
                headers=JAN,
            ),
            case("GET", "/posts/1", expected={"title": POST["title"]}),
            case(
                "PUT",
                "/posts/1",
                {**POST, "title": "Updated by Anna"},
                headers=ANNA,
                expected={"title": "Updated by Anna"},
            ),
            case(
                "POST",
                "/posts/1/comments",
                {"body": "A great example"},
                status=201,
                headers=JAN,
            ),
            case(
                "GET",
                "/posts/1/with-comments",
                expected={"comments": [{"id": 1, "body": "A great example"}]},
            ),
        ]
        if n == 20:
            result.extend([
                case(
                    "POST",
                    "/posts/1/summarize",
                    expected={"mode": "local simulation, not a language model"},
                ),
                case(
                    "POST",
                    "/posts",
                    {"title": "Bad", "body": "forbiddenword"},
                    status=400,
                    headers=ANNA,
                ),
            ])
        result.extend([
            case("DELETE", "/posts/1", status=403, headers=JAN),
            case("DELETE", "/posts/1", status=204, headers=ANNA),
            case("GET", "/posts/1", status=404),
            case("PUT", "/users/2", {"name": "Jan Updated"}, headers=JAN),
            case("DELETE", "/users/1", status=204, headers=ANNA),
            case("GET", "/users/1", status=404),
        ])
        return result
    raise ValueError("Unknown exercise")
