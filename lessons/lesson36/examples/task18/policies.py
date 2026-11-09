def schedule(autoscaling, group):
    for name, cron, size in (("night", "0 22 * * *", 2), ("morning", "0 6 * * *", 4)):
        autoscaling.put_scheduled_update_group_action(
            AutoScalingGroupName=group, ScheduledActionName=name,
            Recurrence=cron, TimeZone="UTC", DesiredCapacity=size,
        )


def archive_releases(s3, bucket, existing_rules):
    rule = {"ID": "release-archive", "Status": "Enabled",
            "Filter": {"Prefix": "releases/"},
            "Transitions": [{"Days": 90, "StorageClass": "GLACIER"}]}
    rules = [item for item in existing_rules if item.get("ID") != rule["ID"]]
    return s3.put_bucket_lifecycle_configuration(
        Bucket=bucket, LifecycleConfiguration={"Rules": [*rules, rule]}
    )
