import asyncio
from lab_support import event, launch, metric, span

async def producer(queue):
    for number in range(1, 21):
        await asyncio.sleep(0.5)
        await queue.put(number)
        event("put", "producer", str(number))
    for _ in range(2):
        await queue.put(None)

async def consumer(name, queue, processed):
    while True:
        number = await queue.get()
        try:
            if number is None:
                return
            event("get", name, str(number))
            with span(name, f"item-{number}"):
                await asyncio.sleep(0.7)
                processed.append(number)
                event("log", name, f"Processed {number}")
        finally:
            queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=4)
    processed = []
    consumers = [asyncio.create_task(consumer(name, queue, processed))
                 for name in ("consumer-A", "consumer-B")]
    await producer(queue)
    await queue.join()
    await asyncio.gather(*consumers)
    metric("Processed items", len(processed))
    metric("Exactly 1..20", sorted(processed) == list(range(1, 21)))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
