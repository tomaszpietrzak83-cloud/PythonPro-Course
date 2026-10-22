import asyncio
from lab_support import event, launch

async def counter(n):
    for number in range(1, n + 1):
        await asyncio.sleep(1)
        event("log", "counter", str(number))

async def main():
    await counter(3)

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
