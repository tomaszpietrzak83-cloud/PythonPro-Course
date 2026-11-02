import logging


def auto_stop(ec2, dry_run=True):
    actions = []
    for page in ec2.get_paginator("describe_instances").paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                tags = {t["Key"]: t["Value"] for t in instance.get("Tags", [])}
                if (
                    instance["State"]["Name"] != "running"
                    or tags.get("AutoStop", "").lower() != "true"
                ):
                    continue
                ident = instance["InstanceId"]
                logging.info("AutoStop %s dry_run=%s", ident, dry_run)
                if not dry_run:
                    ec2.stop_instances(InstanceIds=[ident])
                actions.append(
                    {
                        "id": ident,
                        "action": "planned" if dry_run else "stop requested",
                    }
                )
    return actions


def demo(work, cloud):
    plan = auto_stop(cloud)
    applied = auto_stop(cloud, dry_run=False)
    return {"plan": plan, "simulated_application": applied}
