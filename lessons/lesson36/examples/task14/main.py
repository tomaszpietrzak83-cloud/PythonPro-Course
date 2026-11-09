def route_after_failures(probes, threshold):
    consecutive = 0
    for second, healthy in probes:
        consecutive = 0 if healthy else consecutive + 1
        if consecutive >= threshold:
            return second, "us-east-1"
    return None, "eu-central-1"


def demo(work):
    probes = [(0, False), (30, False)]
    second, region = route_after_failures(probes, 2)
    assert (second, region) == (30, "us-east-1")
    return {"primary": "eu-central-1", "active": region, "switch_seconds": second,
            "prerequisites": ["Route53 failover health checks", "S3 versioning and replication role",
                              "RDS snapshot copy and restore in us-east-1"]}
