import threading
import time

from lab_support import event, launch, metric, span

numbers = []
counter = 0
lock = threading.Lock()


def append_number(number):
    for _ in range(100_000):
        # @step listlock
        with lock:
            numbers.append(number)


def increment_counter(number):
    global counter
    event("log", f"Thread {number}", "Requesting Lock")
    # @step critical
    with lock:
        with span(f"Thread {number}", "holding Lock"):
            previous = counter
            event("log", f"Thread {number}", f"Read: {previous}")
            time.sleep(0.7)
            counter = previous + 1
            event("log", f"Thread {number}", f"Write: {counter}")


def main(config):
    for function in (append_number, increment_counter):
        threads = [threading.Thread(target=function, args=(n,)) for n in (1, 2)]
        for worker_thread in threads:
            worker_thread.start()
        for worker_thread in threads:
            worker_thread.join()
    metric("List length", len(numbers))
    metric("Counter (expected: 2)", counter)


if __name__ == "__main__":
    launch(main)
