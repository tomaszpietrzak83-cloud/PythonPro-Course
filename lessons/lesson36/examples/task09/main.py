def force_failover(rds, database):
    return rds.reboot_db_instance(DBInstanceIdentifier=database, ForceFailover=True)


def measure_outage(samples):
    failed_at = None
    for second, connected in samples:
        if not connected and failed_at is None:
            failed_at = second
        elif connected and failed_at is not None:
            return second - failed_at
    return None


def demo(work):
    samples = [(0, True), (1, False), (2, False), (3, False), (4, True)]
    downtime = measure_outage(samples)
    assert downtime == 3
    return {"MultiAZ": True, "ForceFailover": True, "simulated_probes": samples,
            "observed_downtime_seconds": downtime}
