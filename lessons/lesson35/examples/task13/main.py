def deployment_pipeline(run, healthy, previous="app:v1", image="app:v2"):
    history = []
    for command in [
        ["git", "clone", "https://example.invalid/training.git", "checkout"],
        ["pytest"],
        ["docker", "build", "-t", image, "."],
        ["docker", "push", image],
        ["ssh", "training", "deploy", image],
    ]:
        history.append(command)
        if run(command) != 0:
            return {"status": "failed", "history": history}
    if not healthy():
        rollback = ["ssh", "training", "deploy", previous]
        history.append(rollback)
        code = run(rollback)
        return {
            "status": "rolled back"
            if code == 0 and healthy()
            else "rollback failed",
            "history": history,
        }
    return {"status": "deployed", "history": history}


def demo(work, cloud):
    # No shell, Docker, ECR or SSH is executed. Exercise all control paths.
    checks = iter([False, True])
    return {
        "success": deployment_pipeline(lambda cmd: 0, lambda: True),
        "test_failure": deployment_pipeline(
            lambda cmd: 1 if cmd == ["pytest"] else 0, lambda: True
        ),
        "recovery": deployment_pipeline(lambda cmd: 0, lambda: next(checks)),
    }
