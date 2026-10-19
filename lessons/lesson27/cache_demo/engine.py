"""Run real homework views with isolated cache keys and measurable results."""

import importlib
import time
from uuid import UUID

from django.conf import settings
from django.core.cache import caches
from django.core.cache.backends.locmem import LocMemCache
from django.db import connection
from django.views.decorators.cache import cache_page

from .catalog import PROJECTS


def parse_options(payload, number):
    """Validate untrusted JSON before using it in cache keys or timeouts."""
    token = UUID(str(payload.get("session", ""))).hex
    generation = int(payload.get("generation", 0))
    if not 0 <= generation <= 1000000:
        raise ValueError("Invalid scenario generation.")
    options = {}
    for field, default in (("ttl", 11), ("detail_ttl", 7)):
        value = payload.get(field, default)
        if (
            isinstance(value, bool)
            or int(value) != float(value)
            or not 1 <= int(value) <= 3600
        ):
            raise ValueError(
                "Cache lifetime must be an integer between 1 and 3600 seconds."
            )
        options[field] = int(value)
    options.update(
        prefix=f"demo:{token}:task{number}:run{generation}",
        token=token,
        task=number,
        scenario=payload.get("scenario", "quick"),
    )
    if options["scenario"] not in ("quick", "homework"):
        raise ValueError("Unknown scenario.")
    return options


class QueryCounter:
    """Django's execution wrapper counts SQL without changing any query."""

    def __init__(self):
        self.count = 0

    def __call__(self, execute, sql, params, many, context):
        self.count += 1
        return execute(sql, params, many, context)


def page_cache_result(request, view, ttl, prefix):
    """Measure actual execution behind Django's cache_page decorator.

    The closure starts as False for EVERY request. Django calls the inner view
    only on MISS. A cached response therefore cannot carry a stale MISS label.
    The creation timestamp travels with the cached response and never restarts
    on HIT. Rendering DRF responses here makes them cacheable immediately.
    """
    executed = False

    def tracked_view(inner_request):
        nonlocal executed
        executed = True
        response = view(inner_request)
        response["X-Demo-Created"] = str(time.time())
        response["X-Demo-TTL"] = str(ttl)
        if hasattr(response, "render"):
            response.render()
        return response

    response = cache_page(ttl, cache="demo", key_prefix=prefix)(tracked_view)(
        request
    )
    if response.status_code >= 400:
        raise ValueError(f"Homework view returned HTTP {response.status_code}.")
    import json

    data = json.loads(response.content)
    created = float(response["X-Demo-Created"])
    stored_ttl = int(response["X-Demo-TTL"])
    return {
        "status": "MISS" if executed else "HIT",
        "data": data,
        "expires_at": created + stored_ttl,
        "ttl": stored_ttl,
    }


def homework_modules():
    app = PROJECTS[settings.DEMO_PROJECT]["app"]
    return importlib.import_module(f"{app}.views"), importlib.import_module(
        f"{app}.models"
    )


def request_for_view(request, method="GET", data=None):
    """Build a DRF-compatible request without making an extra HTTP request.

    The cache key uses a stable path. Random query strings would cause misses
    and would hide the mechanism that this lesson is meant to demonstrate.
    """
    from rest_framework.test import APIRequestFactory

    factory = APIRequestFactory()
    path = request.path + ("detail/" if data == "detail" else "list/")
    if method == "PATCH":
        result = factory.patch(path, data=data, format="json")
    else:
        result = factory.get(path, HTTP_ACCEPT="application/json")
    result.META["HTTP_HOST"] = request.get_host()
    return result


def ensure_demo_data(models):
    """Create one clearly named product only when the project has no products."""
    if not models.Product.objects.exists():
        models.Product.objects.create(
            name="Demo sea glass",
            price="19.90",
            short_description="Created by the Lesson 27 presentation",
        )


def demo_client(models, options):
    """Never edit a student's existing client: each browser owns a demo row."""
    city = "Gdansk" if options["scenario"] == "quick" else "Gdynia"
    client, _ = models.Client.objects.get_or_create(
        email=f"cache-demo-task{options['task']}-{options['token']}@example.invalid",
        defaults={
            "name": "Cache Demo Client",
            "city": city,
            "bank": "Demo Bank",
        },
    )
    return client


def client_result(request, views, models, options, action, demo_cache, client):
    prefix = options["prefix"]

    class DemoClientViewSet(views.ClientViewSet):
        # Reuse the student's retrieve and perform_update implementations.
        detail_cache = demo_cache
        detail_timeout = options["detail_ttl"]
        queryset = models.Client.objects.filter(pk=client.pk)

        def detail_cache_key(self, client_id):
            return f"{prefix}:client:{client_id}"

        def list(self, inner_request, *args, **kwargs):
            # Remove only the fixed-time cache decorator from the original list.
            return views.ClientViewSet.list.__wrapped__(
                self, inner_request, *args, **kwargs
            )

    key = f"{prefix}:client:{client.pk}"
    timestamp_key = key + ":created"
    if action == "list":
        inner = request_for_view(request)
        view = DemoClientViewSet.as_view({"get": "list"})
        return page_cache_result(inner, view, options["ttl"], prefix + ":list")
    if action == "update":
        city = "Sopot" if client.city != "Sopot" else "Hel"
        before = client.city
        inner = request_for_view(request, "PATCH", {"city": city})
        response = DemoClientViewSet.as_view({"patch": "partial_update"})(
            inner, pk=client.pk
        )
        if response.status_code != 200:
            raise ValueError("The demo client could not be updated.")
        demo_cache.delete(timestamp_key)
        return {
            "status": "INVALIDATED",
            "data": {
                "before": before,
                "after": city,
                "client": dict(response.data),
            },
            "expires_at": None,
            "ttl": options["detail_ttl"],
        }
    inner = request_for_view(request, data="detail")
    hit = demo_cache.get(key) is not None
    response = DemoClientViewSet.as_view({"get": "retrieve"})(
        inner, pk=client.pk
    )
    if not hit:
        demo_cache.set(timestamp_key, time.time(), options["detail_ttl"])
    created = demo_cache.get(timestamp_key)
    return {
        "status": "HIT" if hit else "MISS",
        "data": dict(response.data),
        "expires_at": created + options["detail_ttl"] if created else None,
        "ttl": options["detail_ttl"],
    }


def low_level_result(number, options, action, demo_cache):
    key = options["prefix"] + ":value"
    marker = key + ":created"
    if number == 5:
        # clear() flushes this dedicated sandbox, never a project's default cache.
        demo_cache = LocMemCache(
            f"demo:{options['token']}:task5:clear-sandbox", {}
        )
        if action == "write":
            demo_cache.set("first", "sea glass", options["ttl"])
            demo_cache.set("second", "ocean blue", options["ttl"])
            demo_cache.set("created", time.time(), options["ttl"])
        elif action in ("clear", "reset"):
            demo_cache.clear()
        data = {name: demo_cache.get(name) for name in ("first", "second")}
        created = demo_cache.get("created")
        status = (
            "CLEARED"
            if action == "clear"
            else ("WRITE" if action == "write" else "READ")
        )
    else:
        if action == "write":
            value = (
                "hello sea" if options["scenario"] == "quick" else "hello world"
            )
            demo_cache.set(key, value, options["ttl"])
            demo_cache.set(marker, time.time(), options["ttl"])
        elif action == "delete":
            demo_cache.delete_many([key, marker])
        data = {"key": key, "value": demo_cache.get(key)}
        created = demo_cache.get(marker)
        status = {"write": "WRITE", "delete": "DELETED"}.get(
            action, "HIT" if data["value"] is not None else "MISS"
        )
    return {
        "status": status,
        "data": data,
        "expires_at": created + options["ttl"] if created else None,
        "ttl": options["ttl"],
    }


def run_action(request, number, payload):
    options = parse_options(payload, number)
    action = payload.get("action", "read")
    allowed = {
        1: {"probe", "reset"},
        2: {"probe", "reset"},
        3: {"read", "reset"},
        4: {"write", "read", "delete", "reset"},
        5: {"write", "read", "clear", "reset"},
        6: {"read", "reset"},
        7: {"read", "reset"},
        8: {"list", "detail", "update", "reset"},
        9: {"list", "detail", "update", "reset"},
        10: {"read", "reset"},
    }
    if action not in allowed[number]:
        raise ValueError("Unknown action for this task.")
    demo_cache = caches["demo"]
    views, models = homework_modules()
    started = time.perf_counter()
    if action == "reset":
        # A new browser generation makes old page-cache keys unreachable. Their
        # normal TTL removes them later; no private Django key API is required.
        if number in (8, 9):
            client = demo_client(models, options)
            models.Client.objects.filter(pk=client.pk).update(
                city="Gdansk" if options["scenario"] == "quick" else "Gdynia"
            )
        if number == 5:
            low_level_result(number, options, "reset", demo_cache)
        return {
            "status": "RESET",
            "data": {"namespace": options["prefix"]},
            "expires_at": None,
            "ttl": options["ttl"],
            "sql_queries": 0,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
            "server_time": time.time(),
        }
    ensure_demo_data(models)
    # Fixture setup is outside the SQL measurement. The displayed count belongs
    # to the operation being demonstrated, not the adapter's preparation query.
    client = demo_client(models, options) if number in (8, 9) else None
    counter = QueryCounter()
    with connection.execute_wrapper(counter):
        if number in (1, 2):
            key = options["prefix"] + ":probe"
            demo_cache.set(key, "connected", 3)
            value = demo_cache.get(key)
            demo_cache.delete(key)
            result = {
                "status": "CONNECTED",
                "data": {
                    "backend": PROJECTS[settings.DEMO_PROJECT]["backend"],
                    "probe": value,
                    "debug_toolbar": settings.DEBUG_TOOLBAR_INSTALLED,
                },
                "expires_at": None,
                "ttl": None,
            }
        elif number in (4, 5):
            result = low_level_result(number, options, action, demo_cache)
        elif number == 7:
            key = options["prefix"] + ":stats"
            simple_data = {
                "product_count": models.Product.objects.count(),
                "first_five_products": list(
                    models.Product.objects.order_by("id").values_list(
                        "name", flat=True
                    )[:5]
                ),
            }
            complex_data = views.get_complex_product_stats(
                demo_cache, options["ttl"], key
            )
            if complex_data["source"] == "calculated":
                demo_cache.set(key + ":created", time.time(), options["ttl"])
            created = demo_cache.get(key + ":created")
            result = {
                "status": "HIT"
                if complex_data["source"] == "cache"
                else "MISS",
                "data": {
                    "simple_data": simple_data,
                    "complex_data": complex_data,
                },
                "expires_at": created + options["ttl"] if created else None,
                "ttl": options["ttl"],
            }
        elif number in (8, 9):
            result = client_result(
                request, views, models, options, action, demo_cache, client
            )
        else:
            inner = request_for_view(request)
            # __wrapped__ removes cache_page but keeps DRF's @api_view wrapper.
            result = page_cache_result(
                inner,
                views.product_list.__wrapped__,
                options["ttl"],
                options["prefix"],
            )
            if number == 6:
                directory = settings.CACHES["demo"]["LOCATION"]
                result["files"] = [
                    {"name": path.name, "bytes": path.stat().st_size}
                    for path in sorted(directory.glob("*.djcache"))
                ]
                result["directory"] = str(directory)
            if number == 10:
                # A companion key uses the same deadline as the page response.
                # HIT only reads this key, so inspection cannot extend its TTL.
                marker = options["prefix"] + ":redis-lifetime"
                if result["status"] == "MISS":
                    demo_cache.set(marker, "page lifetime", options["ttl"])
                result["redis_ttl"] = demo_cache.ttl(marker)
                from django_redis import get_redis_connection

                result["redis_ping"] = bool(get_redis_connection("demo").ping())
    result.update(
        elapsed_ms=round((time.perf_counter() - started) * 1000, 2),
        sql_queries=counter.count,
        server_time=time.time(),
    )
    return result
