"""Local deployment state exercise. Replace its adapters in a real environment."""
import json
import sys
from pathlib import Path


def deploy(directory, environment, revision, probe=lambda _: True):
    active = directory / f"{environment}.json"
    previous = directory / "previous.json"
    if environment == "production":
        previous.write_text(active.read_text() if active.exists() else "null", encoding="utf-8")
    active.write_text(json.dumps({"revision": revision}), encoding="utf-8")
    if not probe(revision):
        raise RuntimeError("Deployment did not pass its probe")


def rollback(directory):
    active = directory / "production.json"
    previous = directory / "previous.json"
    if previous.exists():
        state = json.loads(previous.read_text(encoding="utf-8"))
        if state is None:
            active.unlink(missing_ok=True)
        else:
            active.write_text(json.dumps(state), encoding="utf-8")


if __name__ == "__main__":
    directory = Path(".deployment-demo")
    directory.mkdir(exist_ok=True)
    if sys.argv[1] == "rollback":
        rollback(directory)
    else:
        deploy(directory, sys.argv[1], sys.argv[2])
