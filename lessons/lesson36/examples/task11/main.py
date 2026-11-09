from collections import Counter
from random import Random


def weighted_records(name, primary, canary):
    return [{"Name": name, "Type": "A", "TTL": 300, "SetIdentifier": target,
             "Weight": weight, "ResourceRecords": [{"Value": ip}]}
            for target, weight, ip in [("primary", 80, primary), ("canary", 20, canary)]]


def demo(work):
    records = weighted_records("test.example.", "192.0.2.10", "192.0.2.20")
    counts = Counter(Random(36).choices(
        [record["SetIdentifier"] for record in records],
        [record["Weight"] for record in records], k=100,
    ))
    assert sum(counts.values()) == 100 and 65 <= counts["primary"] <= 95
    return {"records": records, "independent_dns_choices": dict(counts)}
