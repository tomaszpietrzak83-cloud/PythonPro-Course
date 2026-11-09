from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    dependencies = workflow["jobs"]["build"]["needs"]
    passed = {name: True for name in dependencies}
    failed = {**passed, "test": False}
    assert all(passed[name] for name in dependencies)
    assert not all(failed[name] for name in dependencies)
    return {"requires": dependencies, "build_after_failed_test": False}
