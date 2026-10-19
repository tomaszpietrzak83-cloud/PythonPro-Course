import re
import tempfile
import threading
from pathlib import Path

from lab_support import event, launch, metric, span

total = 0
lock = threading.Lock()


def count_words(file, word):
    global total
    with span(file.name, "read and count"):
        # @step tokens
        tokens = re.findall(r"\w+", file.read_text(encoding="utf-8").casefold())
        result = tokens.count(word.casefold())
        # @step merge
        with lock:
            total += result
        event("log", file.name, f"{word!r}: {result}")


def main(config):
    word = config.get("word", "python")
    with tempfile.TemporaryDirectory() as folder:
        for i, text in enumerate(
            [
                "Python, python! code",
                "code python",
                "A Pythonista is not Python.",
            ]
        ):
            Path(folder, f"text{i + 1}.txt").write_text(text, encoding="utf-8")
        # @step files
        threads = [
            threading.Thread(target=count_words, args=(p, word))
            for p in Path(folder).glob("*.txt")
        ]
        for worker_thread in threads:
            worker_thread.start()
        for worker_thread in threads:
            worker_thread.join()
    metric("Total", total)


if __name__ == "__main__":
    launch(main)
