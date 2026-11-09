def copy_snapshot(backup_rds, source_arn, identifier, kms_key):
    response = backup_rds.copy_db_snapshot(
        SourceDBSnapshotIdentifier=source_arn,
        TargetDBSnapshotIdentifier=identifier,
        SourceRegion="eu-central-1",
        KmsKeyId=kms_key,
    )
    backup_rds.get_waiter("db_snapshot_available").wait(DBSnapshotIdentifier=identifier)
    return response


def configure_replication(s3, source, target, role):
    for bucket in (source, target):
        s3.put_bucket_versioning(Bucket=bucket, VersioningConfiguration={"Status": "Enabled"})
    s3.put_bucket_replication(
        Bucket=source,
        ReplicationConfiguration={"Role": role, "Rules": [
            {"ID": "regional-copy", "Priority": 1, "Status": "Enabled", "Filter": {"Prefix": ""},
             "DeleteMarkerReplication": {"Status": "Disabled"},
             "Destination": {"Bucket": f"arn:aws:s3:::{target}"}}
        ]},
    )


def configure_dns(route53, zone_id, name, primary_ip, backup_ip, health_id):
    primary = {"Name": name, "Type": "A", "TTL": 60, "SetIdentifier": "primary",
               "Failover": "PRIMARY", "HealthCheckId": health_id,
               "ResourceRecords": [{"Value": primary_ip}]}
    backup = {"Name": name, "Type": "A", "TTL": 60, "SetIdentifier": "backup",
              "Failover": "SECONDARY", "ResourceRecords": [{"Value": backup_ip}]}
    return route53.change_resource_record_sets(
        HostedZoneId=zone_id, ChangeBatch={"Changes": [
            {"Action": "UPSERT", "ResourceRecordSet": record} for record in (primary, backup)
        ]},
    )
