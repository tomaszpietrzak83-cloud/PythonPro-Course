import asyncio
import random
from lab_support import event, launch, metric, span

async def contender(name, delay):
    with span(name, "race"):
        try:
            await asyncio.sleep(delay)
            return delay
        except asyncio.CancelledError:
            event("log", name, "Cancelled; cleanup complete")
            raise

async def main():
    rng = random.Random(31)
    tasks = [asyncio.create_task(contender(f"job-{i}", rng.uniform(1, 10)))
             for i in range(5)]
    done, pending = await asyncio.wait(
        tasks, return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)
    metric("First completed delay", min(task.result() for task in done), "s")
    metric("Cancelled tasks", len(pending))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
