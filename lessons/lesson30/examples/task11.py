import queue
import threading
import time

from lab_support import event, launch, metric, span

message_queue = queue.Queue()
stop = threading.Event()


def produce():
    for number in range(1, 11):
        if stop.wait(1):
            break
        # @step put
        message_queue.put(number)
        event("put", "Producer", f"+ {number}", value=number)


def consume():
    while True:
        # @step get
        element = message_queue.get()
        try:
            if element is None:
                return
            event("get", "Consumer", f"− {element}", value=element)
            with span("Consumer", f"processing {element}"):
                time.sleep(1.5)
        finally:
            message_queue.task_done()


def main(config):
    p = threading.Thread(target=produce)
    k = threading.Thread(target=consume)
    p.start()
    k.start()
    time.sleep(10)
    # @step shutdown
    stop.set()
    p.join()
    pending = 0
    while True:
        try:
            message_queue.get_nowait()
            message_queue.task_done()
            pending += 1
        except queue.Empty:
            break
    # @step sentinel
    message_queue.put(None)
    k.join()
    metric("Pending after 10 seconds", pending)
    event(
        "log",
        "Program",
        "Finished the current item; remaining items were set aside.",
    )


if __name__ == "__main__":
    launch(main)
