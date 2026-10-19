"""HTML pages and a small same-origin JSON API for the presentation."""

import json
import os

from django.conf import settings
from django.core.cache import caches
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .catalog import (
    EXPLANATIONS,
    PROJECTS,
    REQUIREMENTS,
    TITLES,
    polish_requirements,
    source_files,
    task_project,
)
from .engine import run_action
from .questions import QUESTION_BANK


def page_context(number=None):
    tasks = [
        {
            "number": n,
            "title": {"en": title[0], "pl": title[1]},
            "port": PROJECTS[task_project(n)]["port"],
            "backend": PROJECTS[task_project(n)]["backend"],
        }
        for n, title in TITLES.items()
    ]
    context = {
        "tasks": tasks,
        "project": settings.DEMO_PROJECT,
        "backend": PROJECTS[settings.DEMO_PROJECT]["backend"],
        "port": settings.DEMO_PORT,
        "number": number,
        "boot": {
            "number": number,
            "port": settings.DEMO_PORT,
            "tasks": tasks,
            "control_port": settings.DEMO_CONTROL_PORT,
        },
    }
    if number:
        context["sources"] = source_files(number)
        original_ttl = {3: 60, 4: 30, 6: 60, 7: 7, 8: 600, 9: 600, 10: 60}.get(
            number, 30
        )
        context["boot"].update(
            title={"en": TITLES[number][0], "pl": TITLES[number][1]},
            requirements={
                "en": REQUIREMENTS[number],
                "pl": polish_requirements()[number],
            },
            explanation={
                "en": EXPLANATIONS[number][0],
                "pl": EXPLANATIONS[number][1],
            },
            questions=QUESTION_BANK[number],
            original_ttl=original_ttl,
        )
    return context


@require_GET
@ensure_csrf_cookie
@never_cache
def home(request):
    return render(request, "cache_demo/home.html", page_context())


@require_GET
@ensure_csrf_cookie
@never_cache
def task(request, number):
    if number not in PROJECTS[settings.DEMO_PROJECT]["tasks"]:
        raise Http404(
            "This task belongs to a different project. Use the home page links."
        )
    return render(request, "cache_demo/task.html", page_context(number))


@require_GET
@never_cache
def health(request):
    """Check storage too: an HTTP server can be up while Redis is unavailable."""
    try:
        backend = caches["demo"]
        key = f"health:{os.getpid()}"
        backend.set(key, "ok", 2)
        connected = backend.get(key) == "ok"
        backend.delete(key)
        data = {
            "online": connected,
            "project": settings.DEMO_PROJECT,
            "backend": PROJECTS[settings.DEMO_PROJECT]["backend"],
            "pid": os.getpid(),
        }
    except Exception as error:
        data = {
            "online": False,
            "project": settings.DEMO_PROJECT,
            "error": type(error).__name__,
        }
    response = JsonResponse(data)
    # Only this read-only status endpoint is cross-origin. Demo actions and
    # mutations use same-origin POST with Django's CSRF protection.
    response["Access-Control-Allow-Origin"] = "*"
    return response


@require_POST
@never_cache
def action(request, number):
    if number not in PROJECTS[settings.DEMO_PROJECT]["tasks"]:
        return JsonResponse(
            {"error": "This task belongs to another project."}, status=404
        )
    try:
        payload = json.loads(request.body)
        if not isinstance(payload, dict):
            raise ValueError("Expected a JSON object.")
        return JsonResponse(run_action(request, number, payload))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        return JsonResponse({"error": str(error)}, status=400)
    except Exception as error:
        # Return a useful failure without exposing credentials or a traceback.
        return JsonResponse(
            {
                "error": "Demo unavailable. Check the database migrations and backend connection.",
                "error_type": type(error).__name__,
            },
            status=503,
        )
