from typing import Annotated

from fastapi import Header, HTTPException, Request
from models import User

DEMO_KEYS = {"demo-anna-key": 1, "demo-jan-key": 2}


async def get_actor(
    request: Request, x_api_key: Annotated[str | None, Header()] = None
):
    user_id = DEMO_KEYS.get(x_api_key)
    if user_id is None:
        raise HTTPException(401, "Use a demonstration API key")
    async with request.app.state.sessions() as session:
        user = await session.get(User, user_id)
        if user is None:
            raise HTTPException(401, "Demo user does not exist")
        return user.id
