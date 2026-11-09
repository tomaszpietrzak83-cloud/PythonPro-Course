def switch(elbv2, group, current_ids, candidate_ids, validate):
    """Validate candidates first, wait for ELB health, then drain the old targets."""
    if not candidate_ids or set(current_ids) & set(candidate_ids):
        raise ValueError("Use nonempty, separate sets of targets")
    if not all(validate(instance) for instance in candidate_ids):
        return False
    current = [{"Id": instance} for instance in current_ids]
    candidates = [{"Id": instance} for instance in candidate_ids]
    elbv2.register_targets(TargetGroupArn=group, Targets=candidates)
    try:
        elbv2.get_waiter("target_in_service").wait(TargetGroupArn=group, Targets=candidates)
    except Exception:
        elbv2.deregister_targets(TargetGroupArn=group, Targets=candidates)
        raise
    elbv2.deregister_targets(TargetGroupArn=group, Targets=current)
    return True
