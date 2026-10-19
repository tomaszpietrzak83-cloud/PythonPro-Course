import multiprocessing as mp

from lab_support import event, launch


def send_name(message_queue, name):
    # @step put
    message_queue.put(name)
    event("log", "Child", f"put({name!r})")


def main(config):
    # The UI form replaces input(); the child has no interactive console.
    name = config.get("name", "Anna")
    # @step queue
    message_queue = mp.Queue()
    process = mp.Process(target=send_name, args=(message_queue, name))
    process.start()
    # @step get
    received = message_queue.get(timeout=10)
    event("log", "Parent", f"Hello, {received}!")
    process.join()
    if process.exitcode != 0:
        raise RuntimeError("The process failed")
    message_queue.close()
    message_queue.join_thread()


if __name__ == "__main__":
    launch(main)
