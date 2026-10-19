import hashlib
import multiprocessing as mp
import tempfile
from pathlib import Path

from lab_support import event, launch, metric, span


def hash_file(name):
    file = Path(name)
    with span(mp.current_process().name, file.name):
        # @step init_hash
        digest = hashlib.sha256()
        # @step hash
        with file.open("rb") as data:
            for chunk in iter(lambda: data.read(65_536), b""):
                digest.update(chunk)
        # @step digest
        return file.name, digest.hexdigest()


def main(config):
    with tempfile.TemporaryDirectory() as folder:
        for number in range(4):
            Path(folder, f"file{number}.bin").write_bytes(
                bytes([number]) * 500_000
            )
        files = [str(p) for p in Path(folder).iterdir()]
        # @step map
        with mp.Pool(processes=2) as pool:
            results = dict(pool.map(hash_file, files))
        for name, digest in results.items():
            event("log", name, digest)
        metric("Hashes", len(results))


if __name__ == "__main__":
    launch(main)
