def rolling_update(health):
    current = ["v1", "v1"]
    minimum_healthy = 1
    unavailable = 0
    for slot, healthy in enumerate(health):
        unavailable += int(len(current) - 1 < minimum_healthy)
        if not healthy:
            return {"versions": ["v1", "v1"], "rollback": True, "unavailable_steps": unavailable}
        current[slot] = "v2"
    return {"versions": current, "rollback": False, "unavailable_steps": unavailable}


def demo(work):
    success = rolling_update([True, True])
    failure = rolling_update([True, False])
    assert success["versions"] == ["v2", "v2"] and failure["rollback"]
    return {"strategy": {"MinHealthyPercentage": 50, "AutoRollback": True},
            "success": success, "failed_probe": failure}
