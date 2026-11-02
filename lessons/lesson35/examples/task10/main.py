import shutil
from datetime import datetime, timedelta, timezone


def backup_with_rotation(source, bucket, s3, now=None):
    now = now or datetime.now(timezone.utc)
    archive = shutil.make_archive(str(source.parent / "backup"), "zip", source)
    key = "backups/" + now.strftime("%Y%m%d_%H%M%S_%f") + ".zip"
    s3.upload_file(archive, bucket, key)
    removed = []
    for page in s3.get_paginator("list_objects_v2").paginate(
        Bucket=bucket, Prefix="backups/"
    ):
        for obj in page.get("Contents", []):
            if obj["LastModified"] < now - timedelta(days=7):
                s3.delete_object(Bucket=bucket, Key=obj["Key"])
                removed.append(obj["Key"])
    return {"uploaded": key, "removed": removed}


def demo(work, cloud):
    source = work / "project"
    source.mkdir()
    (source / "app.txt").write_text("version=1")
    cloud.put_object(Bucket="source", Key="backups/old.zip", Body=b"old")
    cloud.objects["source"]["backups/old.zip"]["LastModified"] -= timedelta(
        days=8
    )
    return backup_with_rotation(source, "source", cloud, now=cloud.now)
