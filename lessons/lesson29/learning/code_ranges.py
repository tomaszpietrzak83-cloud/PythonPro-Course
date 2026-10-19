"""Derive highlighted ranges from Python syntax instead of fixed line counts."""

import ast
import re


def code_ranges(source):
    rows = source.splitlines()
    tree = ast.parse(source)
    ranges = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.stmt):
            continue
        start, end = node.lineno, node.end_lineno
        if isinstance(node, ast.If):
            # Include this branch, rather than all subsequent elif branches.
            end = node.body[-1].end_lineno
        text = "\n".join(rows[start - 1 : end]).strip()
        if (
            isinstance(node, (ast.FunctionDef, ast.ClassDef))
            and node.decorator_list
        ):
            start = min(item.lineno for item in node.decorator_list)
            for decorator in node.decorator_list:
                ranges.append(
                    {
                        "start": decorator.lineno,
                        "end": decorator.end_lineno,
                        "text": "@"
                        + re.sub(
                            r"\s+",
                            "",
                            ast.get_source_segment(source, decorator),
                        ),
                    }
                )
        ranges.append(
            {"start": start, "end": end, "text": re.sub(r"\s+", "", text)}
        )
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
            for key, value in zip(node.value.keys, node.value.values):
                if key is None:
                    continue
                entry = "\n".join(
                    rows[key.lineno - 1 : value.end_lineno]
                ).strip()
                ranges.append(
                    {
                        "start": key.lineno,
                        "end": value.end_lineno,
                        "text": re.sub(r"\s+", "", entry),
                    }
                )
    return ranges
