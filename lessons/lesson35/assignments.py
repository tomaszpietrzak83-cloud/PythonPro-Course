"""Paginated assignments from the original tasks.md without rewriting them."""

import math
import re
from pathlib import Path

ENGLISH = ['Write a Python script using requests to check availability of three websites. Display whether each returns 200 OK and its response time.', 'Create a directory backup script using shutil and datetime. Copy a directory into backups/, append date and time to its name (e.g. backup_20240615_143022), and report success.', 'Use boto3 to list all AWS regions for EC2. Display each region name and endpoint. Configure AWS permissions without storing access keys in code.', 'Write create_s3_bucket(bucket_name, region). Create a new S3 bucket and handle an error when the bucket already exists.', 'Upload every .jpg file from a directory to an S3 bucket. Use pathlib.Path to iterate through the files.', 'List all EC2 instances. Display the instance ID, type, state (e.g. running or stopped), and public IP when present.', 'Parse a log file and count ERROR, WARNING and INFO levels. Return a dictionary. Example: two ERROR records and one INFO record yield ERROR=2, INFO=1.', 'Read AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_DEFAULT_REGION using os.environ. Warn when any is missing.', 'List running EC2 instances, inspect AutoStop=true/false tags, stop those with AutoStop=true, and log every action. This simulates an evening developer cost-saving scheduler. Start with dry_run that only reports planned actions.', 'Extend task 2: upload the backup to S3 instead of copying it locally. Implement rotation by inspecting LastModified and deleting backups older than seven days.', 'Copy all objects from one S3 bucket into another bucket in a different region using boto3 copy_object. This simulates disaster recovery backup.', 'Create AWSCostCalculator. Retrieve EC2 instances and estimate costs from instance type and running time using simplified prices, e.g. t3.micro=$0.01/hour. Return a cost report.', 'Build a deployment pipeline: clone or update a Git repository, run pytest, build a Docker image if tests pass, push to ECR, deploy to EC2 over SSH, run a health check, and roll back if it fails.', 'Build an argparse CLI: create an S3 static website bucket, upload HTML/CSS/JS files with correct Content-Type, configure a public-read bucket policy, and display the website URL. Public access must be an explicit configuration decision.', 'Build infrastructure monitoring every five minutes using schedule or asyncio. Check all EC2 states, EBS disk utilization and HTTP health endpoints; write CSV metrics and send alerts when problems occur.', 'Simulate auto-scaling for twenty iterations. simulate_load() returns random CPU load from 20 to 90 percent. After three consecutive measurements above 70 percent, print a new-instance action. After three below 30 percent, print a stop action. Record action history.', 'Monitor S3 by listing new objects. Download new .jpg or .png images, create thumbnails with Pillow, and upload them under thumbnails/ in the same bucket. This simulates S3 Event plus Lambda.', 'Create ConfigManager backed by JSON. Support dev, staging and production, each with region, instance_type and db_size. deploy(environment) displays planned resources; compare(env1, env2) displays configuration differences.', 'Design disaster recovery: create_snapshot() simulates EC2/RDS snapshots and saves JSON metadata; store_backup_s3() simulates S3 backup in a different region; restore_from_backup(snapshot_id) simulates recovery; test_recovery() tests the process. Log the full operation history.', 'Create a cloud cost optimizer using simulated dictionaries. Analyze EC2 instances and uptime; detect low-utilization instances running 24/7; suggest Reserved Instances and calculate savings; detect stopped instances with attached volumes; write a Markdown recommendation report.']


def assignment(number, adaptation):
    text = Path(__file__).with_name("tasks.md").read_text(encoding="utf-8")
    sections = re.split(r"^## TASK (\d+) - ", text, flags=re.MULTILINE)
    records = {int(sections[i]): sections[i + 1] for i in range(1, len(sections), 2)}
    title, body = records[number].split("\n", 1)
    return dict(
        source="tasks.md",
        title=title.strip(),
        adaptation=adaptation,
        pages={
            "pl": pages(parse_blocks(body)),
            "en": pages(parse_blocks(ENGLISH[number - 1])),
        },
    )


def parse_blocks(text):
    blocks = []
    lines = text.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("```"):
            language = line[3:]
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append(
                {
                    "kind": "code",
                    "text": "\n".join(code),
                    "language": language,
                }
            )
        elif re.match(r"(?:- |\d+\. )", line):
            items = []
            ordered = not line.startswith("- ")
            while i < len(lines) and re.match(r"\s*(?:- |\d+\. )", lines[i]):
                items.append(re.sub(r"^\s*(?:- |\d+\. )", "", lines[i]))
                i += 1
            blocks.append({"kind": "list", "items": items, "ordered": ordered})
            continue
        elif line.startswith("<p"):
            blocks.append(
                {
                    "kind": "note",
                    "text": re.sub(r"<[^>]+>", "", line),
                }
            )
        else:
            paragraph = [line]
            while (
                i + 1 < len(lines)
                and lines[i + 1].strip()
                and not lines[i + 1].lstrip().startswith(("```", "- ", "<p"))
            ):
                i += 1
                paragraph.append(lines[i].strip())
            blocks.append({"kind": "paragraph", "text": " ".join(paragraph)})
        i += 1
    return blocks


def pages(blocks):
    result, current, weight = [], [], 0
    for block in blocks:
        if block["kind"] == "code":
            size = len(block["text"].splitlines()) + 1
        elif block["kind"] == "list":
            size = sum(max(1, math.ceil(len(item) / 90)) for item in block["items"]) + 1
        else:
            size = max(1, math.ceil(len(block["text"]) / 90)) + 1
        if current and weight + size > 14:
            result.append(current)
            current, weight = [], 0
        current.append(block)
        weight += size
    if current:
        result.append(current)
    return result
