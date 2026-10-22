import asyncio
import random
from lab_support import config, event, launch, metric, span

async def operation(delay):
    with span("operation", "deadline"):
        try:
            await asyncio.sleep(delay)
            return "Completed in time"
        finally:
            event("log", "operation", "Cleanup complete")

async def main():
    delay = config().get("delay", 1)
    if delay == "random":
        delay = random.uniform(1, 5)
    metric("Requested delay", round(delay, 3), "s")
    try:
        result = await asyncio.wait_for(operation(delay), timeout=3)
        event("log", "result", result)
        metric("Timeout", False)
    except asyncio.TimeoutError:
        event("log", "result", "Time limit of 3 seconds exceeded")
        metric("Timeout", True)

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
