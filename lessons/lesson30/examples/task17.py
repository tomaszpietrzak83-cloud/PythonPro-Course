import multiprocessing as mp

from lab_support import event, launch, metric


def compute_statistics(connection):
    try:
        # @step receive
        numbers = connection.recv()
        total = sum(numbers)
        # @step reply
        connection.send((total, total / len(numbers)))
        event("log", "Child", "send((total, average))")
    finally:
        connection.close()


def main(config):
    # @step pipe
    parent, child = mp.Pipe()
    process = mp.Process(target=compute_statistics, args=(child,))
    process.start()
    child.close()
    numbers = config.get("numbers", [2, 4, 6, 8])
    parent.send(numbers)
    event("log", "Parent", f"send({numbers})")
    if not parent.poll(10):
        raise TimeoutError("The child process did not respond")
    total, average = parent.recv()
    process.join()
    parent.close()
    metric("Sum", total)
    metric("Mean", average)


if __name__ == "__main__":
    launch(main)
