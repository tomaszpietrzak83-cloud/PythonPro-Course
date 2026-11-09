from pathlib import Path

import yaml

ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load(
        (ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8")
    )
    import shlex
    import subprocess
    import sys

    command = shlex.split(workflow["jobs"]["hello"]["steps"][0]["run"])
    assert command[0] == "echo"
    output = subprocess.check_output(
        [
            sys.executable,
            "-c",
            "import sys; print(*sys.argv[1:])",
            *command[1:],
        ],
        text=True,
    ).strip()
    assert output == "Hello, CI/CD!"
    return {"event": "push", "stdout": output}
