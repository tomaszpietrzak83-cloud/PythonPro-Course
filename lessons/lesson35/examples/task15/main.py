import asyncio
import csv


def monitor_once(collect, health, alert, csv_path):
    rows = collect()
    for row in rows:
        row["http_ok"] = health(row["url"])
        if (
            row["state"] != "running"
            or row["disk_used_percent"] > 85
            or not row["http_ok"]
        ):
            alert(f"Problem: {row['id']}")
    exists = csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "state", "disk_used_percent", "url", "http_ok"],
        )
        if not exists:
            writer.writeheader()
        writer.writerows(rows)
    return rows


async def monitor(collect, health, alert, csv_path, interval=300, cycles=None):
    count = 0
    while cycles is None or count < cycles:
        monitor_once(collect, health, alert, csv_path)
        count += 1
        if cycles is None or count < cycles:
            await asyncio.sleep(interval)


def demo(work, cloud):
    # disk_used_percent is a fixture for an OS/CloudWatch Agent measurement, not EBS capacity.
    alerts = []
    collect = lambda: [
        {
            "id": "i-demo",
            "state": "running",
            "disk_used_percent": 92,
            "url": "http://training.invalid/health",
        }
    ]
    asyncio.run(
        monitor(
            collect,
            lambda url: False,
            alerts.append,
            work / "metrics.csv",
            interval=0.01,
            cycles=2,
        )
    )
    (work / "alerts.log").write_text("\n".join(alerts))
    return {"cycles": 2, "alerts": alerts, "production_interval_seconds": 300}
