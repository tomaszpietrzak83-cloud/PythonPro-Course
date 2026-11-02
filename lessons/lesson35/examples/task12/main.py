from datetime import datetime, timezone
from decimal import Decimal


class AWSCostCalculator:
    # Educational rates only, not an AWS price quote.
    rates = {"t3.micro": Decimal("0.01"), "t3.small": Decimal("0.02")}

    def report(self, ec2, now=None):
        now = now or datetime.now(timezone.utc)
        rows = []
        for page in ec2.get_paginator("describe_instances").paginate():
            for group in page["Reservations"]:
                for item in group["Instances"]:
                    if item["State"]["Name"] != "running":
                        continue
                    hours = max(
                        0, (now - item["LaunchTime"]).total_seconds() / 3600
                    )
                    rate = self.rates.get(item["InstanceType"])
                    cost = (
                        round(Decimal(str(hours)) * rate, 4)
                        if rate is not None
                        else None
                    )
                    rows.append(
                        {
                            "id": item["InstanceId"],
                            "hours": round(hours, 2),
                            "estimated_usd": str(cost)
                            if cost is not None
                            else "unknown type",
                        }
                    )
        return rows


def demo(work, cloud):
    return AWSCostCalculator().report(cloud, cloud.now)
