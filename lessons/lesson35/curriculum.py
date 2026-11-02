"""Assemble source and hover notes from a single current snapshot."""

import ast
from pathlib import Path
from functools import lru_cache

from annotations import build
from assignments import assignment
from course_content import content

ROOT = Path(__file__).resolve().parent


def task_sources(number):
    folder = ROOT / "examples" / f"task{number:02}"
    sources = {
        p.relative_to(folder).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(folder.rglob("*"))
        if p.is_file() and p.suffix in {".py", ".json"} and p.name != "__init__.py"
    }
    sources.update(
        {
            name: (ROOT / "examples" / name).read_text(encoding="utf-8")
            for name in ("demo_support.py", "lab_support.py", "run_task.py")
        }
    )
    return sources


@lru_cache(maxsize=64)
def annotated(source, name):
    return build(source, name)


def ensure_material():
    # Preflight every task on startup; no stale ranges saved in a JSON file.
    for number in range(1, 21):
        for name, source in task_sources(number).items():
            if name.endswith(".py"):
                ast.parse(source, filename=name)
    return False


def lesson(number):
    record = content(number)
    sources = {
        name: annotated(source, name)
        for name, source in task_sources(number).items()
        if name not in {"demo_support.py", "lab_support.py", "run_task.py"}
    }
    record["steps"] = dict(
        file="main.py", source=sources["main.py"]["source"], sources=sources, steps=[]
    )
    record["assignment"] = assignment(number, record.pop("adaptation"))
    return record
