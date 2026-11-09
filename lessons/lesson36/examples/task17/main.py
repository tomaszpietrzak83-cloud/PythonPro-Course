def release(unit_ok, integration_ok, approved, production_ok=True):
    stages = ["unit", "integration"]
    if not unit_ok or not integration_ok:
        return stages + ["notify: test failure"]
    stages += ["staging", "production approval"]
    if approved:
        stages.append("production")
        if not production_ok:
            stages.append("rollback")
    return stages + ["notify"]


def demo(work):
    waiting = release(True, True, False)
    failed = release(True, True, True, False)
    assert "production" not in waiting and "rollback" in failed
    return {"waiting": waiting, "failed_deployment": failed}
