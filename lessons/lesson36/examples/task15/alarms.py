def configure_scaling(autoscaling, cloudwatch, group):
    for suffix, threshold, comparator, adjustment in (
        ("high", 100, "GreaterThanThreshold", 1),
        ("low", 20, "LessThanThreshold", -1),
    ):
        policy = autoscaling.put_scaling_policy(
            AutoScalingGroupName=group, PolicyName=f"connections-{suffix}",
            PolicyType="SimpleScaling", AdjustmentType="ChangeInCapacity",
            ScalingAdjustment=adjustment, Cooldown=120,
        )
        cloudwatch.put_metric_alarm(
            AlarmName=f"{group}-connections-{suffix}", Namespace="Lesson36",
            MetricName="ActiveConnections", Statistic="Average", Period=60,
            EvaluationPeriods=1, Threshold=threshold, ComparisonOperator=comparator,
            AlarmActions=[policy["PolicyARN"]], TreatMissingData="notBreaching",
        )
