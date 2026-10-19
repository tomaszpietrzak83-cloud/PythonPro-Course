import math

from celery.result import AsyncResult
from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename

from .catalog import task_catalog
from .code_ranges import code_ranges
from .tasks import hello_world, multiply


def introduction(request):
    return render(request, "learning/catalog.html", {"catalog": task_catalog()})


def health(request):
    import hashlib

    identity = hashlib.sha256(
        str(settings.BASE_DIR.resolve()).casefold().encode()
    ).hexdigest()
    response = JsonResponse({"app": "lesson29", "workspace": identity})
    response["Cache-Control"] = "no-store"
    return response


def lesson(request, task_number=1):
    if not 1 <= task_number <= 20:
        raise Http404("This task is not implemented yet.")
    files = [
        "learning/tasks.py",
        "learning/views.py",
        "academy/celery.py",
        "academy/urls.py",
        "academy/settings.py",
    ]
    if task_number == 2:
        files.append("learning/static/learning/task-two.js")
    else:
        files.extend(
            [
                "learning/models.py",
                "learning/management/commands/enqueue_tasks.py",
                "run_app.py",
            ]
        )
    files.append("README.md")
    code = []
    ranges = []
    for filename in files:
        source = (settings.BASE_DIR / filename).read_text(encoding="utf-8")
        ranges.append(code_ranges(source) if filename.endswith(".py") else [])
        code.append(
            {
                "name": filename,
                "html": highlight(
                    source,
                    get_lexer_for_filename(filename),
                    HtmlFormatter(nowrap=True),
                ),
            }
        )
    catalog = task_catalog()
    return render(
        request,
        "learning/lesson.html",
        {
            "code_files": code,
            "code_ranges": ranges,
            "broker": (
                "Redis"
                if settings.CELERY_BROKER_URL.startswith("redis")
                else "filesystem"
            ),
            "catalog": catalog,
            "task": catalog[task_number - 1],
            "curriculum": (
                get_curriculum(task_number) if task_number > 2 else None
            ),
        },
    )


# TASK 01
@require_POST
def run_hello(request):
    # The HTTP request publishes a message; the worker executes the function.
    try:
        task = hello_world.delay()
    except Exception:
        return JsonResponse({"error": "broker_unavailable"}, status=503)
    return JsonResponse({"task_id": task.id, "state": "QUEUED"}, status=202)


# TASK 02
@require_POST
def run_multiply(request):
    # Validate form values before publishing a task to the broker.
    try:
        a = float(request.POST.get("a", ""))
        b = float(request.POST.get("b", ""))
        if not all(
            math.isfinite(value) and abs(value) <= 1e12 for value in (a, b)
        ):
            raise ValueError(
                "Numbers must be finite and within the exercise range."
            )
    except (ValueError, TypeError):
        return JsonResponse({"error": "invalid_numbers"}, status=400)
    try:
        task = multiply.delay(a, b)
    except Exception:
        return JsonResponse({"error": "broker_unavailable"}, status=503)
    return JsonResponse({"task_id": task.id, "state": "QUEUED"}, status=202)


# TASK 11
# TASK 14
def task_status(request, task_id):
    result = AsyncResult(str(task_id))
    data = {"task_id": str(task_id), "state": result.state}
    if result.successful():
        data["result"] = result.result
    elif result.failed():
        data["error"] = "task_failed"
    elif result.state == "PROGRESS":
        data["progress"] = result.info
    return JsonResponse(data)


import io
import json
import uuid

import requests
from celery import chain
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.validators import validate_email
from django.db import transaction
from PIL import Image

from . import tasks
from .curriculum import get_curriculum
from .models import (
    EmailNotification,
    LogEntry,
    ProcessingRecord,
    ScrapedPage,
    UploadedImage,
)


@require_POST
def run_exercise(request, task_number):
    if not 3 <= task_number <= 20:
        raise Http404
    try:
        # TASK 03
        # TASK 04
        if task_number in (3, 4):
            result = tasks.log_timestamp.delay()
        # TASK 05
        # TASK 06
        elif task_number in (5, 6):
            result = tasks.count_users.delay()
        # TASK 07
        elif task_number == 7:
            user_id = int(request.POST.get("user_id", "0"))
            if not get_user_model().objects.filter(pk=user_id).exists():
                raise ValueError("Unknown user")
            result = tasks.update_user_last_login.delay(user_id)
        # TASK 08
        elif task_number == 8:
            result = tasks.process_video.delay()
        # TASK 09
        elif task_number == 9:
            output = io.StringIO()
            call_command("enqueue_tasks", stdout=output)
            submissions = json.loads(output.getvalue())
            return JsonResponse(
                {
                    "task_id": submissions[0]["task_id"],
                    "submissions": submissions,
                    "state": "QUEUED",
                },
                status=202,
            )
        # TASK 10
        # TASK 18
        elif task_number in (10, 18):
            recipient = request.POST.get(
                "recipient_email", "student@example.com"
            )
            validate_email(recipient)
            notification = EmailNotification.objects.create(
                recipient_email=recipient,
                subject=request.POST.get("subject", "Celery lesson")[:200],
                body=request.POST.get("body", "Hello from Celery!"),
            )
            result = tasks.send_notification.delay(notification.pk)
        # TASK 11
        elif task_number == 11:
            result = tasks.track_progress.delay()
        # TASK 12
        elif task_number == 12:
            result = tasks.clean_logs.delay()
        # TASK 13
        elif task_number == 13:
            result = tasks.scrape_title.delay()
        # TASK 14
        elif task_number == 14:
            result = tasks.generate_csv.delay()
        # TASK 15
        elif task_number == 15:
            result = tasks.retry_connection.delay()
        # TASK 16
        elif task_number == 16:
            upload = request.FILES.get("image")
            if not upload or upload.size > 5 * 1024 * 1024:
                raise ValueError("Image required, maximum 5 MB")
            with Image.open(upload) as image:
                image.verify()
            upload.seek(0)
            record = UploadedImage.objects.create(image=upload)
            result = tasks.classify_image.delay(record.pk)
        # TASK 17
        elif task_number == 17:
            result = chain(
                tasks.random_number.s(),
                tasks.times_ten.s(),
                tasks.save_number.s(),
            )()
        # TASK 19
        elif task_number == 19:
            response = requests.post(
                "http://127.0.0.1:5559/api/task/async-apply/learning.tasks.hello_world",
                json={"args": []},
                timeout=5,
            )
            response.raise_for_status()
            return JsonResponse(
                {
                    "task_id": response.json()["task-id"],
                    "state": "QUEUED",
                    "via": "Flower API",
                },
                status=202,
            )
        else:
            return create_transaction_record(request)
    except (ValueError, ValidationError, Image.UnidentifiedImageError):
        return JsonResponse({"error": "invalid_input"}, status=400)
    except Exception:
        return JsonResponse({"error": "broker_unavailable"}, status=503)
    payload = {"task_id": result.id, "state": "QUEUED"}
    if task_number == 8:
        payload["message"] = "Przetwarzanie wideo rozpoczęte!"
    return JsonResponse(payload, status=202)


# TASK 20
def create_transaction_record(request):
    task_id = str(uuid.uuid4())
    try:
        with transaction.atomic():
            record = ProcessingRecord.objects.create(
                text=request.POST.get("text", "hello transaction")[:200]
            )
            # TASK 20
            transaction.on_commit(
                lambda: tasks.process_record.apply_async(
                    args=[record.pk], task_id=task_id
                )
            )
            if request.POST.get("rollback") == "yes":
                raise ValueError("Demonstration rollback")
    except ValueError:
        return JsonResponse(
            {
                "state": "ROLLED_BACK",
                "result": "Rollback: no record saved; no task published.",
            }
        )
    return JsonResponse({"task_id": task_id, "state": "QUEUED"}, status=202)


def exercise_data(request, task_number):
    if not 3 <= task_number <= 20:
        raise Http404
    data = {}
    if task_number in (3, 4):
        path = settings.BASE_DIR / "log.txt"
        data["log.txt"] = (
            path.read_text(encoding="utf-8").splitlines()[-12:]
            if path.exists()
            else []
        )
    if task_number in (5, 6, 7, 14):
        data["users"] = list(
            get_user_model()
            .objects.order_by("pk")
            .values("id", "username", "email", "last_login")[:30]
        )
    if task_number in (10, 18):
        data["notifications"] = list(
            EmailNotification.objects.order_by("-pk").values()[:10]
        )
    if task_number == 12:
        data["logs"] = list(
            LogEntry.objects.order_by("-created_at").values()[:20]
        )
    if task_number == 13:
        data["pages"] = list(ScrapedPage.objects.order_by("-pk").values()[:10])
    if task_number == 16:
        data["images"] = list(
            UploadedImage.objects.order_by("-pk").values()[:10]
        )
    if task_number == 20:
        data["records"] = list(
            ProcessingRecord.objects.order_by("-pk").values()[:10]
        )
    schedules = {
        4: "timestamp-every-ten-seconds",
        6: "users-at-23",
        12: "daily-log-cleanup",
        13: "hourly-page-title",
    }
    if task_number in schedules:
        schedule = settings.CELERY_BEAT_SCHEDULE[schedules[task_number]]
        data["schedule"] = {
            "task": schedule["task"],
            "schedule": str(schedule["schedule"]),
            "timezone": settings.TIME_ZONE,
        }
    return JsonResponse(data)
