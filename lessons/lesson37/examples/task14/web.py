import json
import os

from celery import Celery
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_POST
from main import summarize

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "lesson-local")
ROOT_URLCONF = __name__
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
celery = Celery(
    "reports", broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"]
)


@celery.task
def report(values):
    import psycopg
    from psycopg.types.json import Jsonb

    result = summarize(values)
    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        db.execute("CREATE TABLE IF NOT EXISTS reports (result jsonb NOT NULL)")
        db.execute("INSERT INTO reports VALUES (%s)", (Jsonb(result),))
    return result


@require_POST
def enqueue(request):
    try:
        values = json.loads(request.body)["values"]
        if not isinstance(values, list) or any(
            type(v) is not int for v in values
        ):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"error": "Expected an integer list"}, status=400)
    return JsonResponse({"id": report.delay(values).id}, status=202)


def status(request, job):
    result = celery.AsyncResult(job)
    return JsonResponse({
        "state": result.state,
        "result": result.result if result.successful() else None,
    })


urlpatterns = [path("reports", enqueue), path("reports/<str:job>", status)]
