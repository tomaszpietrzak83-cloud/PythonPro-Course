import asyncio
from lab_support import launch, metric, span

async def operation(name, delay):
    with span(name, "Waiting for I/O"):
        await asyncio.sleep(delay)
        return delay

async def main():
    results = await asyncio.gather(operation("A", 1), operation("B", 4), operation("C", 2))
    metric("Delays in input order", str(results))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
