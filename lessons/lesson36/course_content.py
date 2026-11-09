"""Bilingual lesson content and predictions for the local exercises."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROWS = json.loads((ROOT / "material.json").read_text(encoding="utf-8"))
TEACHING = json.loads((ROOT / "teaching.json").read_text(encoding="utf-8"))


def pair(pl, en):
    return {"pl": pl, "en": en}


MODES = {2: 'http', 4: 'mixed'}
DEFAULT = 'AWS'
EXECUTION = {
    "http": ("LOKALNE HTTP", "LOCAL HTTP"),
    "api": ("LOKALNE API · SQLite", "LOCAL API · SQLite"),
    "process": ("LOKALNY PROCES PYTHONA", "LOCAL PYTHON PROCESS"),
    "test": ("LOKALNE TESTY PYTEST", "LOCAL PYTEST EXECUTION"),
    "mixed": ("LOKALNY ZIP · MODEL S3", "LOCAL ZIP · S3 MODEL"),
    "AWS": ("MODEL AWS / PLAN", "AWS MODEL / PLAN"),
    "Docker": ("LOKALNY POKAZ LOGIKI / KONFIGURACJI", "LOCAL LOGIC / CONFIGURATION DEMO"),
    "CI": ("LOKALNA WERYFIKACJA WORKFLOW", "LOCAL WORKFLOW VERIFICATION"),
}
LIMITS = {
    "AWS": ("Pokaz używa lokalnych danych lub adaptera. Funkcje z klientem AWS i plany wymagają własnego środowiska do wykonania w chmurze.", "The demo uses local data or an adapter. Client functions and plans need your own environment to run in AWS."),
    "Docker": ("Pokaz działa na hoście. Dockerfile i Compose są osobnymi plikami do uruchomienia z silnikiem Docker.", "The demo runs on the host. Dockerfile and Compose are separate files for use with a Docker engine."),
    "CI": ("Pokaz działa lokalnie. Pliki CI uruchamiają się po umieszczeniu w odpowiednim katalogu repozytorium i konfiguracji runnera.", "The demo runs locally. CI files run after placement in the appropriate repository directory and runner setup."),
}


def content(number):
    pl, en, forecast_pl, forecast_en = ROWS[number - 1]
    intro_pl, intro_en, q_pl, q_en, answer_pl, answer_en = TEACHING[number - 1]
    prediction = pair(forecast_pl, forecast_en)
    adaptation = pair(*LIMITS[DEFAULT])
    return dict(
        number=number, title=pair(pl, en), intro=pair(intro_pl, intro_en),
        forecast=prediction, takeaway=prediction, watch=pair(intro_pl, intro_en),
        question=pair(q_pl, q_en), answer=pair(answer_pl, answer_en),
        execution=pair(*EXECUTION[MODES.get(number, DEFAULT)]),
        pipeline=pair("Dane wejściowe → sprawdzana operacja → wynik i pliki",
                      "Inputs → observed operation → result and evidence files"),
        adaptation=adaptation, caveat=adaptation,
        extra_question=pair("Który wynik potwierdza wykonanie tego scenariusza?",
                            "Which result verifies this scenario?"),
        extra_answer=prediction,
        presets=[dict(label="Dane kontrolne / Controlled inputs", value={})],
        terms=[],
    )


ENGLISH = ['Create a PostgreSQL RDS db.t3.micro instance, retain backups for 3 days, wait for availability and take one manual snapshot.', 'Implement GET /health with aiohttp. Check memory usage and return status information as JSON, with HTTP 200 when healthy.', 'Create a security group allowing public HTTP on TCP 80 and HTTPS on TCP 443, with other inbound ports denied.', 'Zip the application directory, upload the archive to S3 and report its object URL.', 'Use AWS CLI to inspect EC2 instances, RDS status and S3 buckets. Save the results in aws-resources.txt.', 'Create a Route 53 A record for test.yourdomain.com pointing to 1.2.3.4 with a 300-second TTL.', 'Create an HTTP target group on port 8000 with /health checks every 30 seconds.', 'Create a read replica, wait for available and print its endpoint.', 'Configure Multi-AZ RDS, probe database connectivity, trigger forced failover and report observed downtime.', 'Create an ALB in two subnets, configure health checks and an HTTP listener on port 80, register two EC2 instances and inspect the traffic split.', 'Configure weighted Route 53 records at 80/20 and sample 100 requests or independent DNS selections.', 'Schedule RDS snapshots at 02:00, delete owned snapshots older than seven days, log operations and send a completion email.', 'Design a rolling deployment with at least two instances, a launch template and user data, 50% minimum healthy capacity, load-balancer checks and rollback. Measure downtime.', 'Design failover from eu-central-1 to us-east-1 using Route 53 health checks, S3 replication and RDS snapshot copies. Simulate an outage and measure the switch time.', 'Publish active connections every minute to CloudWatch. Scale out above 100 and scale in below 20. Test the policy under load.', 'Use blue and green Auto Scaling Groups with a target group. Validate green, switch traffic and retain an instant rollback path.', 'Create a GitHub Actions pipeline with unit and integration tests, staging, production approval, Slack notifications and rollback.', 'Estimate savings from night scaling, Spot for batch work, S3 archival and RDS reservations. Provide a CloudWatch cost dashboard and a report.', 'Plan CloudWatch Logs, rate, error and latency metrics, and alarms above 80% CPU for five minutes, 5% errors and 2 s latency. Route alerts to SNS.', 'Plan production IaC with three AZs, private/public subnets, RDS Multi-AZ and replicas, TLS ALB, ASG 2–20, weighted DNS, S3, monitoring, CI/CD, IAM, Secrets Manager and WAF.']
