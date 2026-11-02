import json

from auth import get_actor
from demo_support import get_db, runtime_file
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
from lab_support import event
from models import Comment, Post
from schemas import CommentCreate, PostCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/posts", tags=["posts"])


def post_data(post):
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "user_id": post.user_id,
    }


def analyze_sentiment(comment_id, body):
    sentiment = (
        "positive"
        if "great" in body.lower()
        else "negative"
        if "bad" in body.lower()
        else "neutral"
    )
    with runtime_file("sentiment.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(
            json.dumps({
                "comment_id": comment_id,
                "sentiment": sentiment,
                "mode": "rule-based simulation",
            })
            + "\n"
        )
    event("log", "background", f"Simulated sentiment: {sentiment}")


def notify_author(post_id):
    with runtime_file("email.log").open("a", encoding="utf-8") as stream:
        stream.write(f"New comment on post {post_id}; email simulated\n")
    event("log", "background", "Author notification recorded")


@router.post("", status_code=201)
async def create_post(
    data: PostCreate,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        post = Post(**data.model_dump(), user_id=actor)
        db.add(post)
        await db.flush()
    return post_data(post)


@router.get("")
async def list_posts(db: AsyncSession = Depends(get_db)):
    posts = (await db.execute(select(Post).order_by(Post.id))).scalars().all()
    return [post_data(post) for post in posts]


@router.get("/{post_id}")
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if post is None:
        raise HTTPException(404, "Post not found")
    return post_data(post)


@router.put("/{post_id}")
async def replace_post(
    post_id: int,
    data: PostCreate,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        post = await db.get(Post, post_id)
        if post is None:
            raise HTTPException(404, "Post not found")
        if post.user_id != actor:
            raise HTTPException(403, "Only the author may edit")
        post.title = data.title
        post.body = data.body
    return post_data(post)


@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        post = await db.get(Post, post_id)
        if post is None:
            raise HTTPException(404, "Post not found")
        if post.user_id != actor:
            raise HTTPException(403, "Only the author may delete")
        await db.delete(post)
    return Response(status_code=204)


@router.post("/{post_id}/comments", status_code=201)
async def add_comment(
    post_id: int,
    data: CommentCreate,
    background_tasks: BackgroundTasks,
    actor: int = Depends(get_actor),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        if await db.get(Post, post_id) is None:
            raise HTTPException(404, "Post not found")
        comment = Comment(body=data.body, post_id=post_id, user_id=actor)
        db.add(comment)
        await db.flush()
    background_tasks.add_task(notify_author, post_id)
    background_tasks.add_task(analyze_sentiment, comment.id, comment.body)
    return {"id": comment.id, "body": comment.body}


@router.get("/{post_id}/with-comments")
async def post_with_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    statement = (
        select(Post)
        .options(selectinload(Post.comments))
        .where(Post.id == post_id)
    )
    post = (await db.execute(statement)).scalar_one_or_none()
    if post is None:
        raise HTTPException(404, "Post not found")
    return {
        **post_data(post),
        "comments": [{"id": c.id, "body": c.body} for c in post.comments],
    }


@router.post("/{post_id}/summarize")
async def summarize(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if post is None:
        raise HTTPException(404, "Post not found")
    summary = " ".join(post.body.split()[:12])
    return {
        "summary": summary,
        "mode": "local simulation, not a language model",
    }
