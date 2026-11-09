import os
from pathlib import Path
import subprocess
import sys


def demo(work):
    for _ in range(2):
        subprocess.run([sys.executable, __file__], check=True, env={**os.environ, "DATA_DIR": str(work)})
    lines = (work / "events.log").read_text().splitlines()
    assert len(lines) == 2
    return {"processes": 2, "lines": lines}


if __name__ == "__main__":
    directory = Path(os.getenv("DATA_DIR", "/data"))
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "events.log").open("a", encoding="utf-8") as log:
        log.write("container start\n")
