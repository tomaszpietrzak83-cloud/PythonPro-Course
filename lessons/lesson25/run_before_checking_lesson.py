"""Prepare the shared course environment."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from setup_course import main

if __name__ == "__main__":
    main()
