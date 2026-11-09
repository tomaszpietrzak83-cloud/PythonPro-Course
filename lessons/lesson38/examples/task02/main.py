from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    from subprocess import check_output
    from sys import executable
    
    output = check_output([executable, str(ROOT / "hello.py")], text=True).strip()
    assert output == "Hello, CI/CD!"
    return {"stdout": output}
