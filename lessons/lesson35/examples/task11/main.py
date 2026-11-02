def sync_buckets(source, destination, s3):
    if source == destination:
        raise ValueError("Use two different buckets")
    copied = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=source):
        for obj in page.get("Contents", []):
            s3.copy_object(
                Bucket=destination,
                Key=obj["Key"],
                CopySource={"Bucket": source, "Key": obj["Key"]},
            )
            copied.append(obj["Key"])
    return copied


def demo(work, cloud):
    cloud.put_object(
        Bucket="source", Key="data/report.txt", Body=b"recovery data"
    )
    copied = sync_buckets("source", "recovery-eu-west-1", cloud)
    return {
        "copied": copied,
        "destination_region": "eu-west-1",
        "mode": "simulated",
    }
