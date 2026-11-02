import re
from collections import Counter
from pathlib import Path


def parse_logs(path):
    counts = Counter({"ERROR": 0, "WARNING": 0, "INFO": 0})
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\[[^\]]+\] (ERROR|WARNING|INFO):", line)
        if match:
            counts[match.group(1)] += 1
    return dict(counts)


def demo(work, cloud):
    path = work / "app.log"
    path.write_text(
        "[2024-06-15 10:30] ERROR: Connection failed\n"
        "[2024-06-15 10:31] INFO: Retrying ERROR in body\n"
        "[2024-06-15 10:32] ERROR: Max retries exceeded\n"
    )
    return parse_logs(path)
