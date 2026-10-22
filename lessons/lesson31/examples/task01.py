import asyncio
from lab_support import event, launch

async def main():
    event("log", "greeting", "Ready to learn asyncio!")

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
