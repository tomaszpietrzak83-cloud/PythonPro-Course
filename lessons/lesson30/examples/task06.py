import math
import multiprocessing as mp

from lab_support import event, launch, span


def calculate_factorial():
    with span("Child", "factorial"):
        # @step factorial
        result = math.factorial(10)
        event("log", "Child", f"10! = {result}")


def main(config):
    # @step process
    process = mp.Process(target=calculate_factorial)
    process.start()
    event("log", "Parent", f"Child PID: {process.pid}")
    process.join()
    if process.exitcode != 0:
        raise RuntimeError("The child process failed")


# @step guard
if __name__ == "__main__":
    launch(main)
