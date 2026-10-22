import asyncio
from lab_support import event, launch, metric

def is_prime(number):
    if number < 2:
        return False
    return all(number % divisor != 0
               for divisor in range(2, int(number ** 0.5) + 1))

async def primes(limit):
    for number in range(2, limit + 1):
        if is_prime(number):
            await asyncio.sleep(0.1)
            yield number

async def main():
    results = []
    async for number in primes(100):
        results.append(number)
        event("log", "prime", str(number))
    metric("Prime count", len(results))
    metric("Largest prime", max(results))

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
