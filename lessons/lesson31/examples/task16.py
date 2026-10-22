import asyncio
from collections import deque
from lab_support import event, launch, metric, span

class RateLimiter:
    def __init__(self, limit):
        if limit < 1:
            raise ValueError("Limit must be positive")
        self.limit = limit
        self.timestamps = deque()
        self.lock = asyncio.Lock()

    async def acquire(self):
        loop = asyncio.get_running_loop()
        async with self.lock:
            while True:
                now = loop.time()
                while self.timestamps and now - self.timestamps[0] >= 1:
                    self.timestamps.popleft()
                if len(self.timestamps) < self.limit:
                    self.timestamps.append(now)
                    return now
                await asyncio.sleep(max(0, 1 - (now - self.timestamps[0])))

async def request(name, limiter, grants):
    for attempt in range(2):
        with span(name, f"wait-{attempt}"):
            granted = await limiter.acquire()
        grants.append(granted)
        event("log", name, f"Granted attempt {attempt + 1}")

async def main():
    limiter = RateLimiter(5)
    grants = []
    await asyncio.gather(*(request(f"job-{i}", limiter, grants) for i in range(20)))
    times = sorted(grants)
    valid = all(times[i] - times[i - 5] >= 1 for i in range(5, len(times)))
    metric("Granted requests", len(times))
    metric("Rolling window respected", valid)

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
