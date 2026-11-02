def list_instances(ec2):
    rows = []
    for page in ec2.get_paginator("describe_instances").paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                rows.append(
                    dict(
                        id=instance["InstanceId"],
                        type=instance["InstanceType"],
                        state=instance["State"]["Name"],
                        ip=instance.get("PublicIpAddress"),
                    )
                )
    return rows


def demo(work, cloud):
    return list_instances(cloud)
