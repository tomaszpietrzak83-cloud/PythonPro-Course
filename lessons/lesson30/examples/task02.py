import threading
import time

from lab_support import event, launch, span


def greet(number):
    with span(f"Thread {number}", "work"):
        event("log", f"Thread {number}", f"I am thread number {number}")
        time.sleep(0.6)


def main(config):
    threads = []
    # @step args
    for number in range(1, 6):
        worker_thread = threading.Thread(target=greet, args=(number,))
        threads.append(worker_thread)
        worker_thread.start()
    # @step join
    for worker_thread in threads:
        worker_thread.join()


if __name__ == "__main__":
    launch(main)
