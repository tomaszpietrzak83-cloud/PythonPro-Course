"""Small observation layer. Examples also run directly from a terminal."""

import json
import os
import threading
import time
from contextlib import contextmanager


def config():
    return json.loads(os.environ.get("LESSON36_INPUT", "{}"))


def event(kind, actor, label, **data):
    message = dict(
        kind=kind,
        actor=actor,
        label=label,
        at=time.perf_counter(),
        pid=os.getpid(),
        thread=threading.current_thread().name,
        **data,
    )
    # One write per event; UI retains the timestamps from each participant.
    os.write(1, (json.dumps(message, ensure_ascii=False) + "\n").encode("utf-8"))


@contextmanager
def span(actor, label, **data):
    event("start", actor, label, **data)
    try:
        yield
    finally:
        event("end", actor, label, **data)


def metric(label, value, unit="", group=""):
    event("metric", "result", label, value=value, unit=unit, group=group)


def measured(label, function):
    start = time.perf_counter()
    result = function()
    metric(label, round(time.perf_counter() - start, 4), "s")
    return result


def launch(main):
    def thread_error(args):
        event("error", args.thread.name, str(args.exc_value))

    threading.excepthook = thread_error
    event("boot", "program", "START")
    started = time.perf_counter()
    main(config())
    metric("Elapsed time", round(time.perf_counter() - started, 4), "s")
    event("done", "program", "END")
