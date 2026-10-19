"""Regression checks for real cache behavior, isolation and invalidation."""

import json
import time
from unittest import skipUnless
from uuid import uuid4

from django.conf import settings
from django.core.cache import caches
from django.test import TestCase, override_settings

from .catalog import PROJECTS


@override_settings(ALLOWED_HOSTS=["127.0.0.1", "testserver"])
class DemoTests(TestCase):
    def setUp(self):
        self.options = {
            "session": str(uuid4()),
            "generation": 0,
            "scenario": "quick",
            "ttl": 2,
            "detail_ttl": 2,
        }

    def action(self, number, action, **changes):
        response = self.client.post(
            f"/demo/api/{number}/",
            json.dumps({**self.options, **changes, "action": action}),
            content_type="application/json",
            HTTP_HOST="127.0.0.1",
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIn("no-store", response["Cache-Control"])
        return response.json()

    def test_pages_and_wrong_port(self):
        for number in PROJECTS[settings.DEMO_PROJECT]["tasks"]:
            response = self.client.get(
                f"/task/{number}/", HTTP_HOST="127.0.0.1"
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'id="demo-boot"')
        wrong = next(
            n
            for n in range(1, 11)
            if n not in PROJECTS[settings.DEMO_PROJECT]["tasks"]
        )
        self.assertEqual(
            self.client.get(
                f"/task/{wrong}/", HTTP_HOST="127.0.0.1"
            ).status_code,
            404,
        )

    def test_backend_hit_and_reset_isolation(self):
        number = {"l27_pro": 3, "l27_pro_2": 6, "l27_pro_3": 10}[
            settings.DEMO_PROJECT
        ]
        # Redis integration requires the actual server; never replace it with a fake.
        if number == 10:
            try:
                from django_redis import get_redis_connection

                get_redis_connection("demo").ping()
            except Exception:
                self.skipTest("Real Redis server is unavailable.")
        caches["default"].set("homework-isolation-probe", "keep", 30)
        first = self.action(number, "read")
        second = self.action(number, "read")
        self.assertEqual((first["status"], second["status"]), ("MISS", "HIT"))
        self.assertEqual(first["expires_at"], second["expires_at"])
        self.assertEqual(second["sql_queries"], 0)
        time.sleep(2.1)
        self.assertEqual(self.action(number, "read")["status"], "MISS")
        self.action(number, "reset", generation=1)
        fresh = self.action(number, "read", generation=1)
        self.assertEqual(fresh["status"], "MISS")
        self.assertEqual(
            caches["default"].get("homework-isolation-probe"), "keep"
        )
        caches["default"].delete("homework-isolation-probe")
        if number == 6:
            self.assertTrue(first["files"])

    def test_invalid_timeout_and_csrf(self):
        from django.test import Client

        number = PROJECTS[settings.DEMO_PROJECT]["tasks"][0]
        response = self.client.post(
            f"/demo/api/{number}/",
            json.dumps({**self.options, "ttl": 0}),
            content_type="application/json",
            HTTP_HOST="127.0.0.1",
        )
        self.assertEqual(response.status_code, 400)
        protected = Client(enforce_csrf_checks=True)
        response = protected.post(
            f"/demo/api/{number}/",
            "{}",
            content_type="application/json",
            HTTP_HOST="127.0.0.1",
        )
        self.assertEqual(response.status_code, 403)

    @skipUnless(
        settings.DEMO_PROJECT == "l27_pro", "Main project exercises only."
    )
    def test_key_expiration_and_clear_sandbox(self):
        self.action(4, "write", ttl=1)
        self.assertEqual(self.action(4, "read")["status"], "HIT")
        time.sleep(1.1)
        self.assertEqual(self.action(4, "read")["status"], "MISS")
        self.action(4, "write")
        self.action(5, "write")
        result = self.action(5, "clear")
        self.assertEqual(result["data"], {"first": None, "second": None})
        self.assertEqual(self.action(4, "read")["status"], "HIT")

    @skipUnless(
        settings.DEMO_PROJECT == "l27_pro", "Main project exercises only."
    )
    def test_selective_cache_still_executes_simple_queries(self):
        first = self.action(7, "read", ttl=10)
        second = self.action(7, "read", ttl=10)
        self.assertEqual((first["status"], second["status"]), ("MISS", "HIT"))
        self.assertGreater(first["elapsed_ms"], 2900)
        self.assertGreater(second["sql_queries"], 0)
        self.assertEqual(first["expires_at"], second["expires_at"])

    @skipUnless(
        settings.DEMO_PROJECT == "l27_pro", "Main project exercises only."
    )
    def test_patch_invalidates_detail_but_preserves_cached_list(self):
        first_list = self.action(9, "list", ttl=30)
        detail = self.action(9, "detail")
        hit = self.action(9, "detail")
        self.assertEqual(hit["status"], "HIT")
        self.assertEqual(hit["sql_queries"], 0)
        updated = self.action(9, "update")
        fresh = self.action(9, "detail")
        stale = self.action(9, "list", ttl=30)
        self.assertEqual(fresh["status"], "MISS")
        self.assertNotEqual(detail["data"]["city"], fresh["data"]["city"])
        self.assertEqual(fresh["data"]["city"], updated["data"]["after"])
        self.assertEqual(stale["status"], "HIT")
        self.assertEqual(stale["data"], first_list["data"])
