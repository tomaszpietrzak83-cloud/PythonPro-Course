"""Read reviewed teaching material and refuse source/explanation mismatches."""

import ast
import contextlib
import io
import json
import threading
from pathlib import Path

from assignments import assignment

ROOT = Path(__file__).resolve().parent
MATERIAL_LOCK = threading.Lock()


def layout_only_change(before, after):
    """Allow formatting/import sorting and removal of unused imports, not code edits."""
    old, new = ast.parse(before), ast.parse(after)

    def signature(tree):
        used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)}
        imports = {}
        body = []
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    name = alias.asname or (alias.name.split('.')[0] if isinstance(node, ast.Import) else alias.name)
                    imports[name] = (getattr(node, 'module', None), alias.name, getattr(node, 'level', 0))
            else:
                body.append(node)
        return ast.dump(ast.Module(body=body, type_ignores=[])), imports, used

    old_body, old_imports, old_used = signature(old)
    new_body, new_imports, new_used = signature(new)
    return (old_body == new_body
            and all(old_imports.get(name) == binding for name, binding in new_imports.items())
            and all(name in new_imports or name not in old_used | new_used for name in old_imports))


def ensure_material():
    """Refresh ranges after layout changes; require review for actual code changes."""
    with MATERIAL_LOCK:
        records = json.loads((ROOT / 'material.json').read_text(encoding='utf-8'))
        changed = False
        for record in records:
            folder = ROOT / 'examples' / f'task{record["number"]:02}'
            for name, data in record['steps']['sources'].items():
                source = (folder / name).read_text(encoding='utf-8')
                if source == data['source']:
                    continue
                if not layout_only_change(data['source'], source):
                    raise ValueError(f'Zmieniono kod zadania {record["number"]}, {name}. Sprawdź objaśnienia i uruchom lessons/lesson33/create_material.py.')
                changed = True
        if changed:
            from create_material import build
            with contextlib.redirect_stdout(io.StringIO()):
                build()
        return changed


def task_sources(number):
    folder = ROOT / "examples" / f"task{number:02}"
    sources = {
        path.relative_to(folder).as_posix(): path.read_text(encoding="utf-8")
        for path in folder.rglob("*.py")
        if path.name != "__init__.py"
    }
    sources.update({
        name: (ROOT / "examples" / name).read_text(encoding="utf-8")
        for name in ("demo_support.py", "lab_support.py", "run_task.py")
    })
    return sources


def lesson(number):
    if not 1 <= number <= 20:
        raise ValueError("Unknown task")
    record = json.loads((ROOT / "material.json").read_text(encoding="utf-8"))[
        number - 1
    ]
    sources = task_sources(number)
    for name, data in record["steps"]["sources"].items():
        if sources[name] != data["source"]:
            raise ValueError(
                f"Review changed source and regenerate material: task {number}, {name}"
            )
    record["assignment"] = assignment(number, record.pop("adaptation"))
    return record
