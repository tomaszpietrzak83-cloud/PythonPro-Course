import asyncio
from lab_support import launch, metric, span

async def power(number, exponent):
    with span("power", "calculate"):
        await asyncio.sleep(2)
        return number ** exponent

async def main():
    result = await power(5, 3)
    metric("5 ** 3", result)

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
