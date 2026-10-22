import asyncio
from lab_support import launch, metric, span

from aiohttp import ClientSession, ClientTimeout

async def fetch(session, url):
    with span(url.split("/")[-2], "External HTTP"):
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

async def main():
    urls = [f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot" for symbol in ("BTC", "ETH", "LTC")]
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
        results = await asyncio.gather(*(fetch(session, url) for url in urls))
    for data in results:
        metric(data["data"]["base"] + " USD (live)", data["data"]["amount"])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
