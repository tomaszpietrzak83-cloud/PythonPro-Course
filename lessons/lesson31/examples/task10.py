import asyncio
from lab_support import event, launch, span

async def countdown(name, start):
    with span(name, "countdown"):
        for remaining in range(start, 0, -1):
            event("log", name, f"{remaining} seconds left")
            await asyncio.sleep(1)
        event("log", name, "Finished")

async def main():
    await asyncio.gather(
        countdown("A", 5), countdown("B", 3), countdown("C", 7)
    )

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
