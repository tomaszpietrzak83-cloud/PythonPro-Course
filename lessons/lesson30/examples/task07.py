import multiprocessing as mp

from lab_support import event, launch


# @step worker
def calculate_power(number, exponent):
    event("log", "Child", f"{number} ** {exponent} = {number ** exponent}")


def main(config):
    # @step args
    process = mp.Process(
        target=calculate_power, args=(config.get("number", 5), 3)
    )
    process.start()
    process.join()
    if process.exitcode != 0:
        raise RuntimeError("The process failed")


if __name__ == "__main__":
    launch(main)
