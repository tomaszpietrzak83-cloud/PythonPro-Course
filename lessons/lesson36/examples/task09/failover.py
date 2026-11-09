import time


def enable_multi_az(rds, identifier):
    rds.modify_db_instance(DBInstanceIdentifier=identifier, MultiAZ=True, ApplyImmediately=True)
    rds.get_waiter("db_instance_available").wait(DBInstanceIdentifier=identifier)
    instance = rds.describe_db_instances(DBInstanceIdentifier=identifier)["DBInstances"][0]
    if not instance["MultiAZ"]:
        raise RuntimeError("Multi-AZ conversion is still pending")


def observe(probe, trigger, timeout=120, interval=1, *, clock=time.monotonic, sleep=time.sleep):
    """Measure from the first failed probe until the first successful recovery probe."""
    if not probe():
        raise RuntimeError("The baseline connection must work before failover")
    trigger()
    deadline = clock() + timeout
    failed_at = None
    while clock() < deadline:
        healthy = probe()
        now = clock()
        if not healthy and failed_at is None:
            failed_at = now
        if healthy and failed_at is not None:
            return now - failed_at
        sleep(interval)
    return None
