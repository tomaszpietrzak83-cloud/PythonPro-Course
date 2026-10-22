import asyncio
from lab_support import event, launch, metric, span

async def fetch_user_id(username):
    with span("user", "lookup"):
        await asyncio.sleep(1)
        event("log", "user", f"{username} -> 42")
        return 42

async def fetch_posts(user_id):
    with span("posts", "lookup"):
        await asyncio.sleep(1)
        return [user_id * 10 + i for i in range(3)]

async def fetch_comments(post_id):
    with span(f"post-{post_id}", "comments"):
        await asyncio.sleep(1)
        return [f"Comment on post {post_id}"]

async def main():
    user_id = await fetch_user_id("Anna")
    post_ids = await fetch_posts(user_id)
    comments = await asyncio.gather(*(fetch_comments(post) for post in post_ids))
    event("log", "comments", str(comments))
    metric("Posts", len(post_ids))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
