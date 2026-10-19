import multiprocessing as mp
import random

from lab_support import launch, measured, metric, span


def apply_filter(task):
    number, image, variant = task
    with span(f"{variant} · {number}", "filter"):
        # @step filter
        return [[pixel * 1.1 for pixel in row] for row in image]


def main(config):
    side = config.get("side", 300)
    rng = random.Random(30)
    # @step data
    images = [
        [[rng.random() for _ in range(side)] for _ in range(side)]
        for _ in range(10)
    ]
    tasks = [(i, image, "Sequential") for i, image in enumerate(images)]
    sequential_results = measured(
        "Sequential", lambda: list(map(apply_filter, tasks))
    )

    def run_in_parallel():
        # @step pool
        with mp.Pool(processes=2) as pool:
            return pool.map(
                apply_filter,
                [(i, o, "Processes") for i, o in enumerate(images)],
            )

    results = measured(
        "Processes (startup + IPC + computation)", run_in_parallel
    )
    metric("Identical results", results == sequential_results)
    metric("Processed pixels", 10 * side * side)
    # Processes can be slower: images must be transferred through IPC.


if __name__ == "__main__":
    launch(main)
