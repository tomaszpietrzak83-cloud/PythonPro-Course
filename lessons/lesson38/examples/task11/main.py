from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    env = {**workflow["env"], **workflow["jobs"]["show"]["env"]}
    assert env == {"MODE": "job", "REGION": "local"}
    return env
