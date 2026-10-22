import asyncio
import random
from lab_support import event, launch, metric, span

async def ping(host, delay):
    with span(host, "ping"):
        await asyncio.sleep(delay)
        result = f"Host {host} responds"
        event("log", host, result)
        return result

async def main():
    rng = random.Random(31)
    hosts = [f"server-{number}" for number in range(1, 6)]
    results = await asyncio.gather(
        *(ping(host, rng.uniform(0.1, 1.0)) for host in hosts)
    )
    event("log", "results", str(results))
    metric("Responses", len(results))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
