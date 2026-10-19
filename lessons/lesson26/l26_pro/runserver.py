"""Start this project using the shared course environment."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from course_runtime import run_django

if __name__ == "__main__":
    run_django(__file__, default_port=8000)
