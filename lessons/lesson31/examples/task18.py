import asyncio
from lab_support import event, launch, metric, span

async def worker():
    with span("worker", "lifetime"):
        try:
            while True:
                event("log", "worker", "Working...")
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            event("log", "worker", "Cancelled; cleaning up...")
            raise

async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(5)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        event("log", "main", "Cancellation acknowledged")
    metric("Task cancelled", task.cancelled())

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
