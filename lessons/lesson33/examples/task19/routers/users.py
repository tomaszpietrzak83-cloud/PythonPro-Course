from auth import get_actor
from demo_support import get_db
from fastapi import APIRouter, Depends, HTTPException, Response
from models import User
from schemas import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        user = User(**data.model_dump())
        db.add(user)
        await db.flush()
    return {"id": user.id, "name": user.name}


@router.get("")
async def list_users(db: AsyncSession = Depends(get_db)):
    users = (await db.execute(select(User).order_by(User.id))).scalars().all()
    return [{"id": user.id, "name": user.name} for user in users]


@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(404, "User not found")
    return {"id": user.id, "name": user.name}


@router.put("/{user_id}")
async def replace_user(
    user_id: int,
    data: UserCreate,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
    if actor != user_id:
        raise HTTPException(403, "Only the account owner may edit")
    async with db.begin():
        user = await db.get(User, user_id)
        user.name = data.name
    return {"id": user.id, "name": user.name}


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
    if actor != user_id:
        raise HTTPException(403, "Only the account owner may delete")
    async with db.begin():
        user = await db.get(User, user_id)
        await db.delete(user)
    return Response(status_code=204)
