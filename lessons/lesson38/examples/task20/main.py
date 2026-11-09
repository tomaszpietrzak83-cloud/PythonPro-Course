from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    import os
    import subprocess
    import sys
    
    action = yaml.safe_load((ROOT / ".github/actions/my-action/action.yml").read_text(encoding="utf-8"))
    assert action["runs"]["using"] == "composite"
    xml = work / "coverage.xml"
    subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests",
                    "--cov=src", f"--cov-report=xml:{xml}"], cwd=ROOT,
                   env={**os.environ, "COVERAGE_FILE": str(work / ".coverage")}, check=True, capture_output=True)
    badge = work / "coverage.svg"
    subprocess.run([sys.executable, str(ROOT / ".github/actions/my-action/badge.py"), str(xml), str(badge)], check=True)
    assert "coverage" in badge.read_text(encoding="utf-8")
    return {"action": "composite", "artifacts": [xml.name, badge.name]}
