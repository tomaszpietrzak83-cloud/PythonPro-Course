def cutover(active, candidate, ready):
    if candidate not in ready or not ready[candidate]:
        return active
    return candidate


def demo(work):
    before = "blue"
    rejected = cutover(before, "green", {"green": False})
    deployed = cutover(before, "green", {"green": True})
    rollback = cutover(deployed, before, {"blue": True})
    assert (rejected, deployed, rollback) == ("blue", "green", "blue")
    return {"target_group_operations": ["register green", "wait healthy", "drain blue"],
            "rejected": rejected, "deployed": deployed, "rollback": rollback}
