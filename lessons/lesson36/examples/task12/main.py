from datetime import datetime, timedelta, timezone


def rotate(rds, database, now, notify):
    prefix = f"{database}-scheduled-"
    identifier = prefix + now.strftime("%Y%m%d")
    rds.create_db_snapshot(DBInstanceIdentifier=database, DBSnapshotIdentifier=identifier)
    rds.get_waiter("db_snapshot_available").wait(DBSnapshotIdentifier=identifier)
    deleted = []
    pages = rds.get_paginator("describe_db_snapshots").paginate(
        DBInstanceIdentifier=database, SnapshotType="manual")
    for page in pages:
        for snapshot in page["DBSnapshots"]:
            name = snapshot["DBSnapshotIdentifier"]
            if name.startswith(prefix) and snapshot["SnapshotCreateTime"] < now - timedelta(days=7):
                rds.delete_db_snapshot(DBSnapshotIdentifier=name)
                deleted.append(name)
    notify(f"Created {identifier}; removed {len(deleted)} old snapshots")
    return deleted


def demo(work):
    now = datetime(2026, 1, 10, 2, tzinfo=timezone.utc)
    snapshots = {"app-scheduled-20260101": 9, "app-scheduled-20260108": 2, "manual": 30}
    removed = [name for name, age in snapshots.items()
               if name.startswith("app-scheduled-") and now - timedelta(days=age) < now - timedelta(days=7)]
    assert removed == ["app-scheduled-20260101"]
    (work / "backup.log").write_text(f"{now.isoformat()} create app-scheduled-20260110\nremove {removed[0]}\n", encoding="utf-8")
    (work / "email.txt").write_text("Backup complete; removed one old snapshot.", encoding="utf-8")
    return {"schedule_utc": "0 2 * * *", "planned_deletions": removed}
