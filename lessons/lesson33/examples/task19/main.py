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
