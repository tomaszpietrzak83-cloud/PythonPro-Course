from collections import Counter
from itertools import cycle, islice


def distribute(targets, requests):
    healthy = [name for name, ok in targets.items() if ok]
    return dict(Counter(islice(cycle(healthy), requests)))


def provision(elbv2, vpc, subnets, instances):
    lb = elbv2.create_load_balancer(Name="web", Subnets=subnets, Scheme="internet-facing")
    arn = lb["LoadBalancers"][0]["LoadBalancerArn"]
    target = elbv2.create_target_group(Name="web", Protocol="HTTP", Port=8000,
                                       VpcId=vpc, HealthCheckPath="/health")
    group = target["TargetGroups"][0]["TargetGroupArn"]
    elbv2.register_targets(TargetGroupArn=group, Targets=[{"Id": item} for item in instances])
    return elbv2.create_listener(LoadBalancerArn=arn, Protocol="HTTP", Port=80,
                                 DefaultActions=[{"Type": "forward", "TargetGroupArn": group}])


def demo(work):
    counts = distribute({"instance-a": True, "instance-b": True}, 12)
    assert counts == {"instance-a": 6, "instance-b": 6}
    return {"subnets": ["az-a", "az-b"], "listener": 80, "model_distribution": counts}
