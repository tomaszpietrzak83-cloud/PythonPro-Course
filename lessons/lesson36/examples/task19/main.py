def evaluate(cpu, requests, errors, latency):
    return {"cpu": len(cpu) >= 5 and all(value > 80 for value in cpu[-5:]),
            "errors": bool(requests) and errors / requests > 0.05,
            "latency": latency > 2}


def demo(work):
    alarms = evaluate([81, 85, 82, 90, 84], 100, 6, 1.4)
    assert alarms == {"cpu": True, "errors": True, "latency": False}
    (work / "sns-notifications.txt").write_text("\n".join(name for name, active in alarms.items() if active), encoding="utf-8")
    return {"alarms": alarms, "period_seconds": 60, "request_rate_per_minute": 100,
            "latency_seconds": 1.4, "log_group": "/lesson36/web"}
