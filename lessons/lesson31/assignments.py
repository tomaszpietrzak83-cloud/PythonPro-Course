"""Paginated assignments from the original tasks.md without rewriting them."""
import math
import re
from pathlib import Path

ENGLISH = [
    'Write a coroutine that prints "Ready to learn asyncio!" and run it with asyncio.run().',
    'Write counter(n), which prints numbers from 1 through n, one per second. Use asyncio.sleep(1).',
    'Create two coroutines: task1 sleeps 2 seconds and prints completion; task2 sleeps 1 second and prints completion. In main, await them sequentially and measure the execution time.',
    'Modify task 03 to run both coroutines concurrently with asyncio.gather(). Measure and compare execution times.',
    'Write power(number, exponent) which returns exponentiation after a 2-second delay. Await and print the result in main.',
    'Write fetch_weather(city). After 1.5 seconds, return fictional weather data as a dictionary, for example city, temperature 25 and sunny condition.',
    'Using task 06, fetch weather concurrently for Warsaw, Krakow and Gdansk, then print the results.',
    'Write ping(host), simulating a ping with asyncio.sleep(random.uniform(0.1, 1.0)). Return a message that the host responds. Run five different hosts concurrently.',
    'Accept a list of URLs and check their HTTP statuses concurrently using aiohttp.ClientSession. Print each URL and its status. Install aiohttp if needed.',
    'Write countdown(name, start). Every second print the name and remaining seconds. Run three countdowns concurrently with different names and starting times, such as 5, 3 and 7 seconds.',
    'Write long_calculation() which waits a random 2–5 seconds and returns a random integer 1–100. Run ten concurrently, then calculate and print the sum of results.',
    'Run five tasks, each sleeping a random 1–10 seconds and returning its delay. Print the first completed result without waiting for the others. Use asyncio.wait with return_when=asyncio.FIRST_COMPLETED. Cancel the remaining tasks to avoid uncontrolled background work.',
    'Use asyncio.start_server to create a TCP echo server on localhost:8888. When a client connects and sends a message, echo that message and close the connection.',
    'Implement one producer and two consumers using asyncio.Queue. Every 0.5 seconds the producer adds the next integer from 1 to 20. Consumers take items when available and print which consumer processed each item.',
    'Five coroutines concurrently generate log text and write it to one file. Synchronize access so records do not mix, using asyncio.Lock and aiofiles. Install aiofiles if needed.',
    'Create a RateLimiter class with acquire(). Allow at most n calls per second; excess calls must await until allowed. Test with twenty tasks calling acquire in a loop. Use a limit of five per second.',
    'Create dependent coroutines: fetch_user_id(username) returns an ID after 1 second; fetch_posts(user_id) returns post IDs after 1 second; fetch_comments(post_id) returns comments after 1 second. In main fetch the user ID, then posts, then fetch all posts’ comments concurrently. Measure execution time.',
    'Create an infinite worker printing Working once per second. In main let it run for 5 seconds, then call task.cancel(). Handle asyncio.CancelledError in the worker and print a cleanup message before exiting.',
    'Write an async generator yielding successive primes with a delay such as 0.1 seconds. Iterate with async for in main and print primes up to 100.',
    'Write a coroutine sleeping a random 1–5 seconds. Use asyncio.wait_for with a 3-second limit. Catch asyncio.TimeoutError if the operation exceeds the limit and print an appropriate message.',
]


def assignment(number, adaptation):
    text = Path(__file__).with_name('tasks.md').read_text(encoding='utf-8')
    sections = re.split(r'^## TASK (\d+) - ', text, flags=re.MULTILINE)
    records = {int(sections[i]): sections[i + 1] for i in range(1, len(sections), 2)}
    title, body = records[number].split('\n', 1)
    return dict(source='tasks.md', title=title.strip(), adaptation=adaptation,
                pages={'pl': pages(parse_blocks(body)),
                       'en': pages(parse_blocks(ENGLISH[number - 1]))})

def parse_blocks(text):
    blocks = []
    lines = text.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("```"):
            language = line[3:]
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append({"kind": "code", "text": "\n".join(code), "language": language})
        elif re.match(r"(?:- |\d+\. )", line):
            items = []
            ordered = not line.startswith("- ")
            while i < len(lines) and re.match(r"\s*(?:- |\d+\. )", lines[i]):
                items.append(re.sub(r"^\s*(?:- |\d+\. )", "", lines[i]))
                i += 1
            blocks.append({"kind": "list", "items": items, "ordered": ordered})
            continue
        elif line.startswith("<p"):
            blocks.append({"kind": "note", "text": re.sub(r"<[^>]+>", "", line)})
        else:
            paragraph = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].lstrip().startswith(("```", "- ", "<p")):
                i += 1
                paragraph.append(lines[i].strip())
            blocks.append({"kind": "paragraph", "text": " ".join(paragraph)})
        i += 1
    return blocks


def pages(blocks):
    result, current, weight = [], [], 0
    for block in blocks:
        if block["kind"] == "code":
            size = len(block["text"].splitlines()) + 1
        elif block["kind"] == "list":
            size = sum(max(1, math.ceil(len(item) / 90)) for item in block["items"]) + 1
        else:
            size = max(1, math.ceil(len(block["text"]) / 90)) + 1
        if current and weight + size > 14:
            result.append(current)
            current, weight = [], 0
        current.append(block)
        weight += size
    if current:
        result.append(current)
    return result

