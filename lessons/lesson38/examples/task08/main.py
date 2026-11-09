from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    triggers = workflow["on"]
    assert triggers["push"]["branches"] == triggers["pull_request"]["branches"] == ["main"]
    assert "workflow_dispatch" in triggers
    return {"triggers": triggers}
