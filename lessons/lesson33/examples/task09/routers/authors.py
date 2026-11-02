from fastapi import APIRouter

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("")
async def list_authors():
    return [{"id": 1, "name": "Anna"}]
