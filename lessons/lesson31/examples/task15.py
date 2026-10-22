import asyncio
import tempfile
from pathlib import Path
import aiofiles
from lab_support import event, launch, metric, span

async def write_log(number, path, lock):
    with span(f"writer-{number}", "generate"):
        await asyncio.sleep(0.1)
    async with lock:
        with span(f"writer-{number}", "write"):
            async with aiofiles.open(path, "a", encoding="utf-8") as output:
                await output.write(f"Log from coroutine {number}\n")

async def main():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "logs.txt"
        lock = asyncio.Lock()
        await asyncio.gather(*(write_log(i, path, lock) for i in range(1, 6)))
        async with aiofiles.open(path, encoding="utf-8") as source:
            text = await source.read()
        event("log", "file", text)
        lines = text.splitlines()
        metric("Complete lines", len(lines))
        expected = {f"Log from coroutine {i}" for i in range(1, 6)}
        metric("All records intact", set(lines) == expected and len(lines) == 5)

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
