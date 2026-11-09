from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    def ready(branch, passed):
        return branch == "main" and passed
    
    outcomes = [ready("main", True), ready("main", False), ready("feature", True)]
    assert outcomes == [True, False, False]
    return {"outcomes": outcomes, "condition": workflow["jobs"]["test"]["steps"][-1]["if"]}
