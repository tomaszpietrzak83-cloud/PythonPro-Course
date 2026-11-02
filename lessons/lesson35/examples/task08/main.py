import os


def read_environment(environ=None):
    environ = os.environ if environ is None else environ
    report = {}
    for name in [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_DEFAULT_REGION",
    ]:
        value = environ.get(name)
        report[name] = "configured" if value else "WARNING: missing"
        if name == "AWS_DEFAULT_REGION" and value:
            report[name] = value
    return report


def demo(work, cloud):
    return read_environment(
        {"AWS_ACCESS_KEY_ID": "test-only", "AWS_DEFAULT_REGION": "eu-central-1"}
    )
