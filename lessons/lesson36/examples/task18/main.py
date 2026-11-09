from decimal import Decimal


def estimate(hours, on_demand, alternative):
    return Decimal(str(hours)) * (Decimal(str(on_demand)) - Decimal(str(alternative)))


def demo(work):
    savings = {
        "night scaling": estimate(240, "0.04", "0"),
        "spot batch": estimate(120, "0.05", "0.02"),
        "archived storage": estimate(100, "0.025", "0.005"),
        "reserved database": estimate(720, "0.06", "0.04"),
    }
    report = "\n".join(f"- {key}: {value:.2f} USD" for key, value in savings.items())
    (work / "savings.md").write_text("# Monthly estimate (fixture rates)\n" + report, encoding="utf-8")
    assert sum(savings.values()) == Decimal("29.60")
    return {"monthly_usd": str(sum(savings.values())), "dashboard": "CloudWatch billing metric / us-east-1"}
