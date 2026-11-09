"""Bilingual lesson content and predictions for the local exercises."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROWS = json.loads((ROOT / "material.json").read_text(encoding="utf-8"))
TEACHING = json.loads((ROOT / "teaching.json").read_text(encoding="utf-8"))


def pair(pl, en):
    return {"pl": pl, "en": en}


MODES = {1: 'process', 2: 'process', 3: 'http', 4: 'process', 8: 'http', 10: 'api', 11: 'api', 15: 'api', 17: 'process'}
DEFAULT = 'Docker'
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


ENGLISH = ['Write a Dockerfile for Python that prints Hello, Docker!. Build the image and run a container.', 'Read the NAME environment variable and run the image with different values.', 'Run a Python HTTP server on container port 8000 and publish it on host port 3000.', 'Append logs from a container to a volume and check persistence across restarts.', 'Use a multi-stage Dockerfile and compare image sizes with a single-stage build.', 'Use Compose for a Python backend and PostgreSQL database. Verify the connection.', 'Add a PostgreSQL health check and make the backend wait for service_healthy.', 'Join two containers to a custom bridge network and connect using a service name.', 'Build an API using Redis cache. Show an initial source read and a later cache hit.', 'Use FastAPI or Django with PostgreSQL and Compose to implement GET, POST, PUT and DELETE for books.', 'Use Nginx to proxy API calls and serve static files.', 'Define Compose variants with a bind mount and reload for dev, and image-only execution for production.', 'Run user and post services with separate databases and an API gateway that joins their responses.', 'Use Django, Celery, Redis and PostgreSQL. Accept a report job and process it in a separate worker.', 'Expose /metrics and add Prometheus and Grafana to the book API Compose setup.', 'Scale the backend to three replicas and balance requests with Nginx round robin.', 'Build and test a Docker image in GitHub Actions, then publish to Docker Hub after tests pass.', 'Use a Redis Pub/Sub channel to share WebSocket messages across three replicas behind Nginx.', 'Run a one-shot init service that waits for the database, applies migrations and creates a superuser if needed.', 'Build a React, FastAPI, PostgreSQL, Redis and Celery recommendation app using embeddings from OpenAI or local Ollama.']
