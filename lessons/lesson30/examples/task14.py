import hashlib
import shutil
import tempfile
import threading
from pathlib import Path

from lab_support import event, launch, metric, span


def copy_file(source, destination):
    with span(source.name, "copying"):
        event("log", source.name, "Copying file...")
        # @step copy
        shutil.copy2(source, destination / source.name)
        event("log", source.name, "File copied")


def main(config):
    with tempfile.TemporaryDirectory() as folder:
        src, dst = Path(folder, "src"), Path(folder, "dst")
        src.mkdir()
        dst.mkdir()
        for i in range(4):
            (src / f"file{i}.bin").write_bytes(bytes([i]) * 2_000_000)
        files = list(src.iterdir())
        threads = [
            threading.Thread(target=copy_file, args=(p, dst)) for p in files
        ]
        # @step wait
        for worker_thread in threads:
            worker_thread.start()
        for worker_thread in threads:
            worker_thread.join()
        # @step verify
        copies_match = all(
            hashlib.sha256(p.read_bytes()).digest()
            == hashlib.sha256((dst / p.name).read_bytes()).digest()
            for p in files
        )
        metric("Copies match", copies_match)
        metric("Copied files", len(list(dst.iterdir())))


if __name__ == "__main__":
    launch(main)
