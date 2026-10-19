import threading
import time

from lab_support import event, launch, span


# @step worker
def work():
    with span("Thread", "waiting"):
        time.sleep(3)
    event("log", "Thread", "The worker thread has finished!")


def main(config):
    # @step create
    worker_thread = threading.Thread(target=work)
    # @step start
    worker_thread.start()
    event("log", "Main", "The main program is waiting for the thread...")
    # @step join
    with span("Main", "join: waiting"):
        worker_thread.join()


if __name__ == "__main__":
    launch(main)
