def publish_connections(cloudwatch, count):
    cloudwatch.put_metric_data(Namespace="Lesson36", MetricData=[
        {"MetricName": "ActiveConnections", "Value": count, "Unit": "Count"}])


def scale(samples, capacity=2, maximum=20):
    for count in samples:
        if count > 100:
            capacity = min(capacity + 1, maximum)
        elif count < 20:
            capacity = max(capacity - 1, 2)
        yield {"connections": count, "desired": capacity}


def demo(work):
    history = list(scale([110, 100, 20, 19]))
    assert [row["desired"] for row in history] == [3, 3, 3, 2]
    return {"metric_period_seconds": 60, "simulated_scaling": history}
