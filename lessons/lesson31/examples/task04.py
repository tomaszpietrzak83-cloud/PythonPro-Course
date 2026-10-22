import asyncio
from lab_support import event, launch, span

async def operation(name, delay):
    with span(name, "operation"):
        await asyncio.sleep(delay)
        event("log", name, "Completed")

async def main():
    await asyncio.gather(operation("A", 2), operation("B", 1))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
