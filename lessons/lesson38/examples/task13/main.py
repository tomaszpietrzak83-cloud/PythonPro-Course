from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    from graphlib import TopologicalSorter
    graph = {key: [value["needs"]] if "needs" in value else [] for key, value in workflow["jobs"].items()}
    order = list(TopologicalSorter(graph).static_order())
    assert order == ["lint", "test", "build", "deploy"]
    return {"stage_order": order, "deploy": "echo only"}
