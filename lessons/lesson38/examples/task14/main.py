from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    steps = workflow["jobs"]["publish"]["steps"]
    assert steps[2]["run"].startswith("docker run")
    assert steps[3]["with"]["registry"] == "ghcr.io"
    assert steps[4]["if"] == "github.ref == 'refs/heads/main'"
    return {"order": ["build", "test", "login", "push"], "registry": "ghcr.io"}
