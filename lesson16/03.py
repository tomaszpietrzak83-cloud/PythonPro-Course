from fastapi import FastAPI

app = FastAPI()

articles = {
    1: {"name": "pen", "price": "10.5"},
    2: {"name": "pencil", "price": "2.5"},
}

request_data = {
    "method": "GET",
    "path": "/api/articles",
    "headers": {"host": "my-blog.com"},
}


@app.get("/api/articles")
def get_articles():
    return list(articles.values())
