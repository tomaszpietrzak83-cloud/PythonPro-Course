import subprocess

COMMANDS = [
    ["aws", "ec2", "describe-instances", "--output", "json", "--no-cli-pager"],
    ["aws", "rds", "describe-db-instances", "--output", "json", "--no-cli-pager"],
    ["aws", "s3api", "list-buckets", "--output", "json", "--no-cli-pager"],
]


def execute(args):
    return subprocess.run(args, check=True, capture_output=True, text=True, timeout=30).stdout


def inventory(path, runner=execute):
    sections = [f"$ {' '.join(args)}\n{runner(args)}" for args in COMMANDS]
    path.write_text("\n\n".join(sections), encoding="utf-8")
    return len(sections)


def demo(work):
    fixtures = {"ec2": '{"Reservations":[]}', "rds": '{"DBInstances":[]}',
                "s3api": '{"Buckets":[{"Name":"lesson"}]}'}
    count = inventory(work / "aws-resources.txt", lambda args: fixtures[args[1]])
    assert count == 3
    return {"commands": count, "report": "aws-resources.txt"}
