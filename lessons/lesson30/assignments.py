"""Assignment requirements, separate from conceptual introductions."""
import math
import re
from pathlib import Path

SOURCE = Path(__file__).with_name("tasks.md")
CODE_NAMES = {
    "pobierz_dane": "fetch_data", "id_danych": "data_id",
    "potega": "calculate_power", "liczba": "number", "pot": "exponent",
    "suma_calkowita": "total_sum", "licznik": "counter",
    "KontoBankowe": "BankAccount", "saldo": "balance",
    "wplac": "deposit", "wyplac": "withdraw", "kwota": "amount",
    "suma": "total", "srednia": "average",
    "analizuj_sentyment": "analyze_sentiment", "zdanie": "sentence",
    "zastosuj_filtr": "apply_filter", "obraz": "image",
    "Pozytywny": "Positive", "Negatywny": "Negative", "Neutralny": "Neutral",
}
CODE_MESSAGES = {
    "Wątek zakończył pracę!": "The worker thread has finished!",
    "Główny program czeka na wątek...": "The main program is waiting for the thread...",
    "Jestem wątkiem numer [numer]": "I am thread number [number]",
    "Witaj, [imię]!": "Hello, [name]!",
    "Kopiowanie pliku X...": "Copying file X...",
    "Ukończono kopiowanie pliku X": "File X copied",
}

# English wording preserves the requirements of the Polish source.
ENGLISH = [
    "Write a program that creates and starts one thread.\n\nThe thread must:\n\n- wait for 3 seconds,\n- print the message:\n\n```text\nThe worker thread has finished!\n```\n\nMeanwhile, the main program must display:\n\n```text\nThe main program is waiting for the thread...\n```",
    "Start 5 threads. Each thread receives its number from 1 to 5 and prints:\n\n```text\nI am thread number [number]\n```\n\nEnsure the main program waits for all threads to finish.",
    "Write a function:\n\n```python\nfetch_data(data_id)\n```\n\nSimulate retrieval with `time.sleep(2)`. Run it sequentially for 3 different data IDs and measure the time. Then run each call in a separate thread and measure the time again. Compare the results.",
    "Create a program with a global list and 2 threads:\n\n- one appends the number 1 one hundred thousand times,\n- the other appends the number 2 one hundred thousand times.\n\nAfter both finish, check the list length. Is it 200,000? Run the program several times.\n\nMentor note: In CPython, list.append() may behave safely in this test, so the exercise may not expose a race. A shared counter with counter += 1 is a better illustration of a compound update.",
    "Modify task 4 by adding `threading.Lock` to protect appending to the list. Check whether its length is now always correct.",
    "Write a program that starts a separate process. The child must calculate the factorial of 10 and print the result.",
    "Write a function:\n\n```python\ncalculate_power(number, exponent)\n```\n\nRun it in a new process with:\n\n```python\nnumber = 5\nexponent = 3\n```\n\nThe process must print the result.",
    "Create a process that:\n\n- asks for a name with `input()`,\n- sends the name to the parent using `multiprocessing.Queue`.\n\nThe parent receives it and prints:\n\n```text\nHello, [name]!\n```",
    "Sum a large list, for example 10 million elements. Split it into 4 parts and sum each part in a separate thread. Add partial results to the global `total_sum`, protecting access with `threading.Lock`.",
    "Count the total occurrences of a chosen word across all `.txt` files in the current directory. Search each file in a separate thread. Safely add the individual counts to a shared counter.",
    "Implement the producer–consumer problem with a shared thread-safe queue:\n\n```python\nimport queue\n\nq = queue.Queue()\n```\n\nRequirements:\n\n- a producer thread adds an item, such as a random number, every second,\n- a consumer thread takes and prints an item every 1.5 seconds,\n- the program runs for 10 seconds.",
    "Write a CPU-intensive function, for example:\n\n```python\nsum(i * i for i in range(20_000_000))\n```\n\nMeasure the time for:\n\n1. two sequential calls,\n2. two calls using two separate threads,\n3. two calls using two separate processes.\n\nCompare results and explain them in a code comment.",
    "Generate 100 random integers from 1 to 1000. Use `multiprocessing.Pool` to check whether each is prime. `pool.map` must return a list of True/False values. Print how many primes were found.",
    "Copy all files from one directory to another, each in a separate thread. Display progress, for example:\n\n```text\nCopying file X...\nFile X copied\n```\n\nThe main program must not finish until all files have been copied.",
    "Write a web crawler starting from one URL. It must:\n\n- download page content,\n- find links to the same domain,\n- queue those links for visiting,\n- use a thread pool to download pages concurrently,\n- limit the visited pages, for example to 50,\n- use a thread-safe queue and a set of already visited URLs with synchronized access.",
    "Calculate a SHA256 digest for each file in a directory. Use `multiprocessing.Pool` to distribute files among available CPU cores. Print a dictionary mapping each file name to its hash.",
    "Create duplex communication using `multiprocessing.Pipe`. The parent sends a list of numbers. The child:\n\n- calculates their sum,\n- calculates their mean,\n- replies with the tuple below.\n\n```python\n(total, average)\n```\n\nThe parent receives and prints the results.",
    "Create `BankAccount` with a `balance` attribute and methods:\n\n```python\ndeposit(amount)\nwithdraw(amount)\n```\n\nWithdrawal must check that sufficient funds are available. Start 10 threads:\n\n- 5 deposit random amounts,\n- 5 withdraw random amounts.\n\nProtect the methods with a lock to keep the final balance correct.",
    "Prepare 20 sample product reviews and write:\n\n```python\nanalyze_sentiment(sentence)\n```\n\nSimulate an AI API request with:\n\n```python\ntime.sleep(random.uniform(0.5, 2.0))\n```\n\nReturn one random label: `Positive`, `Negative` or `Neutral`. Use `concurrent.futures.ThreadPoolExecutor` to analyse all sentences, collect results and measure elapsed time.",
    "Process 10 images represented by 1000×1000 lists of random numbers. Write:\n\n```python\napply_filter(image)\n```\n\nIterate over every pixel and perform an operation such as `pixel * 1.1` to simulate CPU-bound work. Use `multiprocessing.Pool` to process all 10 images and measure elapsed time. Compare it with sequential execution.",
]

ADAPTATIONS = {
    2: ("Dodano jawne oczekiwanie 0,6 s, aby przebieg wątków był widoczny.", "An explicit 0.6 s wait makes thread execution visible."),
    4: ("Oprócz listy pokazujemy kontrolowany wyścig licznika. Sama lista może nie ujawnić błędu.", "A controlled counter race supplements the list, which may not expose an error."),
    5: ("Pokaz obejmuje blokadę listy oraz licznika, aby różnica była widoczna.", "The demo locks both list and counter to make the difference observable."),
    8: ("Formularz z gotowym imieniem zastępuje input() w procesie bez interaktywnej konsoli.", "A form with prepared names replaces input() in a process without an interactive console."),
    9: ("Domyślnie milion elementów; pełne 10 milionów wybierzesz z listy.", "Default: one million items. Select the full ten million from the list."),
    10: ("Aplikacja tworzy własne trzy pliki demonstracyjne w katalogu tymczasowym.", "The app creates its own three demonstration files in a temporary directory."),
    11: ("Po 10 s zatrzymujemy produkcję i kończymy bieżącą obsługę. Pozostałe elementy są odkładane.", "After ten seconds production stops and the current item finishes. Remaining items are set aside."),
    12: ("Domyślnie 6 milionów; wariant 20 milionów jest gotowy na liście.", "Default: six million. The twenty-million case is available in the preset list."),
    13: ("Pula korzysta z dwóch procesów; stałe ziarno zapewnia powtarzalne dane.", "The pool uses two processes; a fixed seed makes inputs repeatable."),
    14: ("Kopiujemy własne cztery pliki po 2 MB w katalogu tymczasowym.", "The demo copies four prepared 2 MB files in a temporary directory."),
    15: ("Crawler korzysta z lokalnej witryny czterech stron i prawdziwego HTTP. Internet nie jest potrzebny.", "The crawler uses a local four-page site with real HTTP. No Internet is required."),
    16: ("Przygotowane pliki przetwarza pula dwóch procesów.", "A two-process pool handles prepared demonstration files."),
    19: ("To symulacja API. Opinie i etykiety są po angielsku; nie korzystamy z modelu AI.", "This is an API simulation. Reviews and labels are English; no AI model is called."),
    20: ("Domyślnie obrazy 300×300; pełne 1000×1000 są dostępne z listy.", "Default: 300×300 images. Full 1000×1000 images are available in the preset list."),
}


def english_code(text):
    for old, new in CODE_MESSAGES.items():
        text = text.replace(old, new)
    return re.sub(r"\b(?:" + "|".join(CODE_NAMES) + r")\b",
                  lambda match: CODE_NAMES[match.group()], text)


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
            blocks.append({"kind": "code", "text": english_code("\n".join(code)), "language": language})
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
    # Inline source-code references also follow the English naming convention.
    for block in blocks:
        for key in ("text",):
            if key in block and block["kind"] != "code":
                block[key] = re.sub(r"`([^`]+)`", lambda m: "`" + english_code(m.group(1)) + "`", block[key])
        if "items" in block:
            block["items"] = [re.sub(r"`([^`]+)`", lambda m: "`" + english_code(m.group(1)) + "`", item) for item in block["items"]]
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


def assignment(number):
    text = SOURCE.read_text(encoding="utf-8")
    sections = re.split(r"^## TASK (\d+) - ", text, flags=re.MULTILINE)
    records = {int(sections[i]): sections[i + 1] for i in range(1, len(sections), 2)}
    title, body = records[number].split("\n", 1)
    pl_blocks, en_blocks = parse_blocks(body), parse_blocks(ENGLISH[number - 1])
    note = ADAPTATIONS.get(number)
    return {"source": "tasks.md", "title": title.strip(),
            "pages": {"pl": pages(pl_blocks), "en": pages(en_blocks)},
            "adaptation": {"pl": note[0], "en": note[1]} if note else None}
