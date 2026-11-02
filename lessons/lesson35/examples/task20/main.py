def optimize_costs(
    instances, hourly_rate=0.01, reserved_discount=0.30, ebs_gb_month=0.08
):
    lines = [
        "# Cloud cost recommendations",
        "",
        "Educational rates; estimates are not an AWS quote.",
        "",
    ]
    for item in instances:
        ident = item["id"]
        if (
            item["state"] == "running"
            and item["hours_month"] >= 720
            and item["cpu"] < 10
        ):
            saving = round(
                item["hours_month"] * hourly_rate * reserved_discount, 2
            )
            lines.append(
                f"- {ident}: low utilization, runs 24/7. Right-size first; RI scenario saves ${saving}/month (30% assumption)."
            )
        if item["state"] == "stopped" and item["volume_gb"]:
            cost = round(item["volume_gb"] * ebs_gb_month, 2)
            lines.append(
                f"- {ident}: attached EBS {item['volume_gb']} GB still costs an estimated ${cost}/month. Review data before removal."
            )
    return "\n".join(lines)


def demo(work, cloud):
    report = optimize_costs(
        [
            {
                "id": "i-idle",
                "state": "running",
                "hours_month": 720,
                "cpu": 5,
                "volume_gb": 20,
            },
            {
                "id": "i-stopped",
                "state": "stopped",
                "hours_month": 0,
                "cpu": 0,
                "volume_gb": 50,
            },
        ]
    )
    (work / "recommendations.md").write_text(report, encoding="utf-8")
    return {"report": report}
