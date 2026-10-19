import multiprocessing as mp
import random

from lab_support import event, launch, metric, span


# @step prime
def is_prime(n):
    if n < 2:
        return False
    return all(n % divisor != 0 for divisor in range(2, int(n**0.5) + 1))


def check_number(n):
    with span(f"Proces {mp.current_process().name}", f"n={n}"):
        return is_prime(n)


def main(config):
    rng = random.Random(30)
    data = [rng.randint(1, 1000) for _ in range(100)]
    # @step pool
    with mp.Pool(processes=2) as pool:
        results = pool.map(check_number, data)
    metric("Prime numbers", sum(results))
    event("log", "Results", str(list(zip(data, results))))


if __name__ == "__main__":
    launch(main)
