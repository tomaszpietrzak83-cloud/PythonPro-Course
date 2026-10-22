import asyncio
from lab_support import launch, metric

from aiohttp import ClientSession, ClientTimeout

async def main():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            metric("Bitcoin USD (live)", data["data"]["amount"])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
