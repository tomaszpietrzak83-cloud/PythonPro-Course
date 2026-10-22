import asyncio
from lab_support import event, launch, metric, span

async def fetch_weather(city):
    with span(city, "weather"):
        await asyncio.sleep(1.5)
        return {"city": city, "temperature": 25, "condition": "sunny"}

async def main():
    weather = await fetch_weather("Warsaw")
    event("log", "weather", str(weather))
    metric("Temperature", weather["temperature"], "°C")

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
