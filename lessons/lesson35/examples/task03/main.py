def list_regions(ec2):
    return [
        {"region": r["RegionName"], "endpoint": r["Endpoint"]}
        for r in ec2.describe_regions(AllRegions=True)["Regions"]
    ]


def demo(work, cloud):
    return list_regions(cloud)
