"""Press Play in VS Code to start the complete Lesson 27 presentation."""

import sys
from pathlib import Path

# Resolve imports from this file, so Play works regardless of VS Code's cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cache_demo.run_demo import main

if __name__ == "__main__":
    # run_demo owns startup, shutdown and the clickable terminal URL.
    # Keeping this file small makes the Play entry point easy to explain.
    print("Starting Lesson 27 Cache Lab...", flush=True)
    main()
