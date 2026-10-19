import multiprocessing as mp
import threading

from lab_support import event, launch, measured, span


def calculate_squares(n, name):
    with span(name, "CPU: sum of squares"):
        # @step cpu
        result = sum(i * i for i in range(n))
        event("log", name, f"Sum: {result}")


def run_workers(worker_type, n):
    # @step workers
    tasks = [
        worker_type(
            target=calculate_squares, args=(n, f"{worker_type.__name__} {i}")
        )
        for i in (1, 2)
    ]
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
        if getattr(task, "exitcode", 0) != 0:
            raise RuntimeError("The process failed")


def main(config):
    n = config.get("size", 6_000_000)
    # @step benchmark
    measured(
        "Sequential",
        lambda: [calculate_squares(n, "Sequential") for _ in range(2)],
    )
    measured("Threads", lambda: run_workers(threading.Thread, n))
    measured("Processes", lambda: run_workers(mp.Process, n))
    # Results depend on cores, system load and process startup costs.
    # Overlapping thread lifetimes do not prove parallel CPU execution.


if __name__ == "__main__":
    launch(main)
