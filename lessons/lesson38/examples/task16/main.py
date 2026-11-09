from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    def simulate(secret):
        return {"deployed": bool(secret), "display": "***" if secret else "missing"}
    
    missing = simulate("")
    present = simulate("fixture-secret")
    assert not missing["deployed"] and present["display"] == "***"
    return {"missing": missing, "present": present}
