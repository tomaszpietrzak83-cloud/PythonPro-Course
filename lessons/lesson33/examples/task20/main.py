from demo_support import database_lifespan
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models import Base
from routers import posts, users
from sqlalchemy.exc import IntegrityError

app = FastAPI(lifespan=database_lifespan(Base), title="Mini Blog API")
app.include_router(users.router)
app.include_router(posts.router)


@app.exception_handler(IntegrityError)
async def conflict(request: Request, error: IntegrityError):
    return JSONResponse({"detail": "Conflicting data"}, status_code=409)


@app.middleware("http")
async def moderate(request: Request, call_next):
    if request.method in {"POST", "PUT", "PATCH"}:
        body = await request.body()
        if len(body) > 64000:
            return JSONResponse({"detail": "Body too large"}, status_code=413)
        if b"forbiddenword" in body.lower():
            return JSONResponse(
                {"detail": "Demo moderation rejected content"}, status_code=400
            )
    return await call_next(request)
