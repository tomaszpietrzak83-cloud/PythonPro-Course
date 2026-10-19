"""Only explicitly reviewed comments; never infer prose from nested calls."""
import ast
import json
from pathlib import Path

REVIEW_PATH = Path(__file__).with_name("reviewed_slides.json")


def selected_nodes(source, start, end, number, key):
    nodes = [n for n in ast.walk(ast.parse(source))
             if isinstance(n, ast.stmt) and start <= n.lineno <= end
             and not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                      and isinstance(n.value.func, ast.Name)
                      and n.value.func.id in {"event", "metric"}
                      and (number, key) not in {(1, "worker"), (7, "worker")})]
    result = []
    rows = source.splitlines()
    for node in sorted(nodes, key=lambda n: n.lineno):
        last = (node.body[0].lineno - 1 if isinstance(node,
                (ast.With, ast.For, ast.If, ast.FunctionDef)) else node.end_lineno)
        result.append({"start": node.lineno, "end": last,
                       "code": "\n".join(rows[node.lineno-1:last]).strip()})
    return result


def details(source, start, end, number, key, body):
    nodes = selected_nodes(source, start, end, number, key)
    record = json.loads(REVIEW_PATH.read_text(encoding="utf-8"))[f"{number}.{key}"]
    actual = "\n".join(source.splitlines()[start-1:end]).strip()
    if actual != record["code"]:
        raise ValueError(f"Comment needs review after source change: {number}.{key}")
    if body != record["body"]:
        raise ValueError(f"Explanation needs review after text change: {number}.{key}")
    # A single instruction already has its authored explanation on the main slide.
    if len(nodes) <= 1:
        if record["details"]:
            raise ValueError(f"Unexpected detail notes: {number}.{key}")
        return []
    if [n["code"] for n in nodes] != [n["code"] for n in record["details"]]:
        raise ValueError(f"Detail selection changed: {number}.{key}")
    return [dict(start=node["start"], end=node["end"], body=note["body"])
            for node, note in zip(nodes, record["details"], strict=True)]
