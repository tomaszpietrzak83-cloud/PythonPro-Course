def configure_alarms(cloudwatch, topic_arn, group):
    specs = [
        ("cpu", "AWS/EC2", "CPUUtilization", 80, 5, [{"Name": "AutoScalingGroupName", "Value": group}]),
        ("errors", "Lesson36", "ErrorPercent", 5, 1, []),
        ("latency", "Lesson36", "LatencySeconds", 2, 1, []),
    ]
    for suffix, namespace, metric, threshold, periods, dimensions in specs:
        cloudwatch.put_metric_alarm(
            AlarmName=f"{group}-{suffix}", Namespace=namespace, MetricName=metric,
            Dimensions=dimensions, Statistic="Average", Period=60,
            EvaluationPeriods=periods, DatapointsToAlarm=periods,
            ComparisonOperator="GreaterThanThreshold", Threshold=threshold,
            AlarmActions=[topic_arn], TreatMissingData="notBreaching",
        )
