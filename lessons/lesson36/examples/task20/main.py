import json
from graphlib import TopologicalSorter

RESOURCES = {
    "vpc-3az": [],
    "subnets-public-private": ["vpc-3az"],
    "least-privilege-iam": [],
    "secrets-manager": ["least-privilege-iam"],
    "rds-multi-az": ["subnets-public-private", "secrets-manager"],
    "read-replicas": ["rds-multi-az"],
    "s3-versioning-lifecycle": ["least-privilege-iam"],
    "alb-https": ["subnets-public-private"],
    "asg-2-20": ["alb-https", "least-privilege-iam"],
    "route53-90-10": ["alb-https", "asg-2-20"],
    "waf": ["alb-https"],
    "cloudwatch": ["asg-2-20", "rds-multi-az"],
    "github-actions-oidc": ["least-privilege-iam", "asg-2-20"],
}


def apply_plan(handlers):
    """Invoke explicitly supplied boto3 provisioning functions in dependency order."""
    missing = RESOURCES.keys() - handlers.keys()
    if missing:
        raise ValueError(f"Missing resource handlers: {sorted(missing)}")
    return {
        name: handlers[name]()
        for name in TopologicalSorter(RESOURCES).static_order()
    }


def demo(work):
    order = list(TopologicalSorter(RESOURCES).static_order())
    assert order.index("rds-multi-az") < order.index("read-replicas")
    (work / "infrastructure-plan.json").write_text(
        json.dumps(RESOURCES, indent=2), encoding="utf-8"
    )
    return {
        "plan_order": order,
        "regions_az": 3,
        "scaling": [2, 20],
        "dns_weights": [90, 10],
    }
