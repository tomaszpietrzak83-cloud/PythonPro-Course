import threading
import time

from lab_support import launch, measured, span


def fetch_data(number, variant):
    with span(f"{variant} · {number}", "waiting for data"):
        time.sleep(2)


def main(config):
    # @step sequential
    def run_sequentially():
        for number in range(1, 4):
            fetch_data(number, "Sequential")

    # @step concurrent
    def run_concurrently():
        threads = [
            threading.Thread(target=fetch_data, args=(number, "Threads"))
            for number in range(1, 4)
        ]
        for worker_thread in threads:
            worker_thread.start()
        for worker_thread in threads:
            worker_thread.join()

    measured("Sequential", run_sequentially)
    measured("Threads", run_concurrently)


if __name__ == "__main__":
    launch(main)
