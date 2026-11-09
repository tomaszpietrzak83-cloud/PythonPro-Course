from ipaddress import IPv4Address


def change_batch(name, address, ttl=300):
    record = {"Name": name.rstrip(".") + ".", "Type": "A", "TTL": ttl,
              "ResourceRecords": [{"Value": str(IPv4Address(address))}]}
    return {"Changes": [{"Action": "UPSERT", "ResourceRecordSet": record}]}


def update_record(route53, zone_id, name, address):
    return route53.change_resource_record_sets(
        HostedZoneId=zone_id, ChangeBatch=change_batch(name, address)
    )


def demo(work):
    batch = change_batch("test.yourdomain.com", "1.2.3.4")
    assert batch["Changes"][0]["ResourceRecordSet"]["TTL"] == 300
    return batch
