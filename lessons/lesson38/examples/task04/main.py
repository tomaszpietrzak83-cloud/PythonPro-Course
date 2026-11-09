from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    from subprocess import run
    from sys import executable
    
    result = run([executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                  str(ROOT / "tests")], capture_output=True, text=True, check=True)
    return {"jobs": list(workflow["jobs"]), "pytest": result.stdout.strip()}
