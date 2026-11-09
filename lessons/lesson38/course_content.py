"""Bilingual lesson content and predictions for the local exercises."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROWS = json.loads((ROOT / "material.json").read_text(encoding="utf-8"))
TEACHING = json.loads((ROOT / "teaching.json").read_text(encoding="utf-8"))


def pair(pl, en):
    return {"pl": pl, "en": en}


MODES = {1: 'process', 2: 'process', 4: 'test', 10: 'test', 17: 'process', 20: 'test'}
DEFAULT = 'CI'
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


ENGLISH = ['Create a push-triggered workflow that prints Hello, CI/CD!.', 'Set up Python 3.11 and execute a script containing hello().', 'Create requirements.txt with requests and pytest and install it in CI.', 'Write the addition test in tests/test_math.py and run pytest.', 'Cache pip downloads with a key derived from requirements.txt.', 'Run a Python 3.9, 3.10 and 3.11 test matrix.', 'Install flake8 and lint the src directory.', 'Configure push and pull request triggers for main and a manual dispatch trigger.', 'Create lint, test and build jobs. Build needs both earlier jobs to pass.', 'Export pytest results as JUnit XML and upload them as an artifact.', 'Declare workflow and job environment variables and print the effective values.', 'Print Ready to deploy! only after successful tests on main.', 'Build a four-job CI/CD pipeline with lint, coverage tests, Docker build and an echo-based deployment.', 'Build a Docker image, test it in a container and publish it to GHCR after success.', 'Create a GitLab pipeline with build, test and deploy stages, dependency cache and JUnit results.', 'Pass API_KEY through GitHub secrets and simulate deployment while logging only a fixed mask.', 'Schedule pip-audit for 03:00 UTC and open an issue only when vulnerabilities are found.', 'Combine three operating systems with three Python versions and demonstrate a matrix exclusion.', 'Authenticate to AWS with OIDC, publish to ECR and deploy a new ECS task revision.', 'Create a composite GitHub Action that runs tests, creates a coverage badge and is invoked from a workflow.']
