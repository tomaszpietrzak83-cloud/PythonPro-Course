from pathlib import Path

import yaml


def demo(work):
    root = Path(__file__).parent
    config = yaml.safe_load((root / ".gitlab-ci.yml").read_text(encoding="utf-8"))
    assert config["stages"] == ["build", "test", "deploy"]
    assert config["tests"]["artifacts"]["reports"]["junit"] == "results.xml"
    return {"stages": config["stages"], "cache": config["cache"], "artifact": "results.xml"}
