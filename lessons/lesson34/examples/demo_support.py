"""Local evidence files and resilient fan-out for the real demonstrations."""

import os
from pathlib import Path


def runtime_file(name):
    folder = Path(
        os.environ.get(
            "LESSON34_WORKDIR",
            Path(__file__).resolve().parents[1] / ".runtime" / "manual",
        )
    )
    folder.mkdir(parents=True, exist_ok=True)
    return folder / name


async def broadcast(connections, text):
    for connection in tuple(connections):
        if connection.closed:
            connections.discard(connection)
            continue
        try:
            await connection.send_str(text)
        except (ConnectionError, RuntimeError):
            connections.discard(connection)
