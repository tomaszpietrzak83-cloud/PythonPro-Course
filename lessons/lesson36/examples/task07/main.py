def target_group(vpc_id):
    return {"Name": "web", "Protocol": "HTTP", "Port": 8000,
            "VpcId": vpc_id, "TargetType": "instance", "HealthCheckPath": "/health",
            "HealthCheckIntervalSeconds": 30, "Matcher": {"HttpCode": "200"}}


def provision(elbv2, vpc_id):
    return elbv2.create_target_group(**target_group(vpc_id))


def demo(work):
    config = target_group("vpc-demo")
    assert (config["Port"], config["HealthCheckPath"], config["HealthCheckIntervalSeconds"]) == (8000, "/health", 30)
    return config
