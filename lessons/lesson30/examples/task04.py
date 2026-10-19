import threading
import time

from lab_support import event, launch, metric, span

numbers = []
counter = 0
barrier = threading.Barrier(2)


def append_number(number):
    # @step append
    for _ in range(100_000):
        numbers.append(number)


def lose_update(number):
    global counter
    with span(f"Thread {number}", "read -> write"):
        # @step read
        previous = counter
        event("log", f"Thread {number}", f"Read: {previous}")
        # @step barrier
        barrier.wait()
        time.sleep(0.7)
        # @step write
        counter = previous + 1
        event("log", f"Thread {number}", f"Write: {counter}")


def main(config):
    for function, arguments in [(append_number, [1, 2]), (lose_update, [1, 2])]:
        threads = [
            threading.Thread(target=function, args=(n,)) for n in arguments
        ]
        for worker_thread in threads:
            worker_thread.start()
        for worker_thread in threads:
            worker_thread.join()
    metric("List length", len(numbers))
    metric("Counter (expected: 2)", counter)


if __name__ == "__main__":
    launch(main)
