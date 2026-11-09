from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    from hashlib import sha256
    requirements = (ROOT / "requirements.txt").read_bytes()
    before = sha256(requirements).hexdigest()
    after = sha256(requirements + b"\nhttpx\n").hexdigest()
    assert before != after
    return {"before": before, "after": after}
