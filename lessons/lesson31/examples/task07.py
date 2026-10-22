import asyncio
from lab_support import event, launch, metric, span

async def fetch_weather(city):
    with span(city, "weather"):
        await asyncio.sleep(1.5)
        return {"city": city, "temperature": 25, "condition": "sunny"}

async def main():
    cities = ["Warsaw", "Krakow", "Gdansk"]
    results = await asyncio.gather(*(fetch_weather(city) for city in cities))
    for weather in results:
        event("log", weather["city"], str(weather))
    metric("Cities", len(results))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
