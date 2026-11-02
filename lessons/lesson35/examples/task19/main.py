import hashlib
import json
import uuid


def create_snapshot(work, data, history):
    ident = "snapshot-" + uuid.uuid4().hex
    payload = json.dumps(data, sort_keys=True).encode()
    snapshot = {
        "id": ident,
        "ec2": "simulated-ec2",
        "rds": "simulated-rds",
        "data": data,
        "sha256": hashlib.sha256(payload).hexdigest(),
    }
    path = work / (ident + ".json")
    path.write_text(json.dumps(snapshot, indent=2))
    history.append("Created simulated EC2/RDS snapshot " + ident)
    return snapshot


def store_backup_s3(snapshot, s3, bucket, history):
    s3.put_object(
        Bucket=bucket,
        Key=snapshot["id"] + ".json",
        Body=json.dumps(snapshot).encode(),
    )
    history.append("Stored snapshot in simulated secondary-region S3")


def restore_from_backup(snapshot_id, s3, bucket, history):
    snapshot = json.loads(
        s3.get_object(Bucket=bucket, Key=snapshot_id + ".json")["Body"].read()
    )
    digest = hashlib.sha256(
        json.dumps(snapshot["data"], sort_keys=True).encode()
    ).hexdigest()
    if digest != snapshot["sha256"]:
        raise ValueError("Snapshot checksum mismatch")
    history.append("Restored and checked " + snapshot_id)
    return snapshot["data"]


def test_recovery(work, s3):
    history = []
    original = {"application": "v1", "records": [1, 2, 3]}
    snapshot = create_snapshot(work, original, history)
    store_backup_s3(snapshot, s3, "recovery-eu-west-1", history)
    restored = restore_from_backup(
        snapshot["id"], s3, "recovery-eu-west-1", history
    )
    assert restored == original
    (work / "recovery.log").write_text("\n".join(history))
    return {"verified": restored == original, "history": history}


def demo(work, cloud):
    return test_recovery(work, cloud)
