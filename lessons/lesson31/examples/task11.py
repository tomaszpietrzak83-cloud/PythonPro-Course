import asyncio
import random
from lab_support import event, launch, metric, span

async def calculate(name, delay, value):
    with span(name, "calculate"):
        await asyncio.sleep(delay)
        event("log", name, str(value))
        return value

async def main():
    rng = random.Random(31)
    jobs = [calculate(f"job-{i}", rng.uniform(2, 5), rng.randint(1, 100))
            for i in range(10)]
    results = await asyncio.gather(*jobs)
    event("log", "results", str(results))
    metric("Sum", sum(results))
    metric("Count", len(results))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
