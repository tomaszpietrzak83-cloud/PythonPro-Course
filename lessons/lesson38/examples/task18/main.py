from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    from itertools import product
    matrix = workflow["jobs"]["test"]["strategy"]["matrix"]
    before = [{"os": os, "python": python} for os, python in product(matrix["os"], matrix["python"])]
    after = [combo for combo in before if combo not in matrix["exclude"]]
    assert len(before) == 9 and len(after) == 8
    return {"baseline": len(before), "scheduled": len(after), "matrix": after}
