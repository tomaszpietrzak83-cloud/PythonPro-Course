"""Start this project using the shared course environment."""
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from course_runtime import run_django

if __name__ == "__main__":
    subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent.parent / "update_docs.py")],
        check=True,
    )
    run_django(__file__, default_port=8000)
