"""Run one offline scenario; retain actual artifacts in its own directory."""

import argparse
import importlib.util
import json
import tempfile
import time
from pathlib import Path

from lab_support import event, metric, span

ROOT = Path(__file__).resolve().parent


def load_task(number):
    if not 1 <= number <= 20:
        raise ValueError("Task must be in 1..20")
    spec = importlib.util.spec_from_file_location(
        f"task{number:02}", ROOT / f"task{number:02}" / "main.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(number):
    runtime = ROOT.parent / ".runtime"
    runtime.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f"task{number:02}-", dir=runtime))
    started = time.perf_counter()
    event(
        "boot",
        "program",
        "Local workshop demonstration",
    )
    with span("python", f"Task {number:02}"):
        result = load_task(number).demo(work)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    (work / "result.json").write_text(output, encoding="utf-8")
    event("log", "result", output)
    for path in sorted(work.rglob("*")):
        if path.is_file() and path.suffix in {
            ".json",
            ".txt",
            ".csv",
            ".log",
            ".md",
            ".html", ".yml", ".yaml", ".conf", ".sh", ".xml", ".svg",
        }:
            event(
                "file",
                "filesystem",
                path.name,
                file_name=path.relative_to(work).as_posix(),
                file_body=path.read_text(encoding="utf-8")[:16000],
            )
    metric("Elapsed time", round(time.perf_counter() - started, 4), "s")
    metric("Evidence files", sum(p.is_file() for p in work.rglob("*")))
    event("done", "program", "END")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, choices=range(1, 21))
    args = parser.parse_args()
    run(args.number)
