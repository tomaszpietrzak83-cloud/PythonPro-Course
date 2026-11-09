from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    from importlib.metadata import version
    requirements = (ROOT / "requirements.txt").read_text().splitlines()
    assert requirements == ["requests", "pytest"]
    return {"installed_locally": {name: version(name) for name in requirements}}
