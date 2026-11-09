from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    import subprocess
    import sys
    import json
    sample = work / "audit.json"
    sample.write_text(json.dumps({"dependencies": [{"name": "fixture", "vulns": [{"id": "DEMO-001"}]}]}), encoding="utf-8")
    issue = work / "issue.md"
    subprocess.run([sys.executable, str(ROOT / "report.py"), str(sample), str(issue)], check=True)
    assert "DEMO-001" in issue.read_text(encoding="utf-8")
    return {"cron": workflow["on"]["schedule"][0]["cron"], "local_issue_draft": issue.name}
