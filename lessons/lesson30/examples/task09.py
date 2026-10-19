import threading

from lab_support import event, launch, metric, span

total_sum = 0
lock = threading.Lock()


def sum_chunk(chunk, number):
    global total_sum
    with span(f"Thread {number}", "partial sum"):
        # @step local
        partial_sum = sum(chunk)
    # @step merge
    with lock:
        total_sum += partial_sum
    event("log", f"Thread {number}", f"Partial sum: {partial_sum}")


def main(config):
    n = config.get("size", 1_000_000)
    data = list(range(n))
    # @step chunks
    threads = [
        threading.Thread(
            target=sum_chunk, args=(data[i * n // 4 : (i + 1) * n // 4], i + 1)
        )
        for i in range(4)
    ]
    for worker_thread in threads:
        worker_thread.start()
    for worker_thread in threads:
        worker_thread.join()
    metric("Sum", total_sum)
    metric("Expected sum", n * (n - 1) // 2)


if __name__ == "__main__":
    launch(main)
