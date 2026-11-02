"""Integration tests for source/teaching consistency and actual Uvicorn/PG demos."""

import ast
import json
import subprocess
import sys
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from curriculum import lesson, task_sources, layout_only_change
from django.test import Client


def execute(number):
    result = subprocess.run(
        [sys.executable, str(ROOT / "examples/run_task.py"), str(number)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=40,
    )
    if result.returncode:
        raise AssertionError(f"Task {number}: {result.stderr}")
    return [
        json.loads(line)
        for line in result.stdout.splitlines()
        if line.startswith("{")
    ]


class LessonTests(unittest.TestCase):
    def test_formatting_refresh_preserves_code_review_boundary(self):
        original = 'from math import sqrt, sin\nfrom json import loads\n\ndef example():\n    return sqrt(4)\n'
        formatted = 'from json import loads\nfrom math import sqrt\n\n\ndef example():\n    return sqrt(\n        4,\n    )\n'
        self.assertTrue(layout_only_change(original, formatted))
        self.assertFalse(layout_only_change(original, formatted.replace('4,', '9,')))
        self.assertFalse(layout_only_change(original, formatted.replace('from math import sqrt', 'from cmath import sqrt')))
        self.assertFalse(layout_only_change(original, formatted.replace('from math import sqrt\n', '')))

    def test_material_matches_every_task_and_file(self):
        for n in range(1, 21):
            record = lesson(n)
            self.assertTrue(record["forecast"]["pl"])
            self.assertTrue(record["takeaway"]["en"])
            self.assertTrue(record["pipeline"]["pl"])
            self.assertTrue(record["assignment"]["pages"]["pl"])
            self.assertTrue(record["assignment"]["pages"]["en"])
            sources = task_sources(n)
            represented = set()
            for step in record["steps"]["steps"]:
                self.assertGreaterEqual(step["start"], 1)
                self.assertLessEqual(step["start"], step["end"])
                self.assertLessEqual(
                    step["end"], len(sources[step["file"]].splitlines())
                )
                represented.add((step["file"], step["start"]))
                for language in ("pl", "en"):
                    self.assertGreater(len(step["body"][language]), 30)
            for file, source in record["steps"]["sources"].items():
                for node in ast.walk(ast.parse(source["source"])):
                    if isinstance(node, ast.stmt):
                        self.assertIn((file, node.lineno), represented)
            quick = record["steps"].get("quick", [])
            self.assertLessEqual(len(quick), 20)
            if len(record["steps"]["steps"]) > 20:
                self.assertTrue(quick)
            for step in quick:
                self.assertIn(step["file"], sources)
                self.assertLessEqual(
                    step["end"], len(sources[step["file"]].splitlines())
                )

    def test_actual_twenty_demonstrations(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            reports = dict(zip(range(1, 21), pool.map(execute, range(1, 21))))
        for n, events in reports.items():
            self.assertEqual(events[0]["kind"], "boot")
            self.assertEqual(events[-1]["kind"], "done")
            self.assertTrue(
                any(
                    e["kind"] == "metric"
                    and e["label"] == "Verified HTTP cases"
                    for e in events
                )
            )
            responses = [e for e in events if e["actor"] == "response"]
            self.assertTrue(responses)
            self.assertTrue(all("response_body" in e for e in responses))
        responses = lambda n: [
            e for e in reports[n] if e["actor"] == "response"
        ]
        self.assertEqual([e["http_status"] for e in responses(2)], [200, 422])
        self.assertEqual(
            [e["http_status"] for e in responses(6)], [201, 200, 200, 204, 404]
        )
        self.assertEqual(
            [e["http_status"] for e in responses(10)], [401, 200, 200, 200, 401]
        )
        for n in (19, 20):
            self.assertTrue(any(e["http_status"] == 403 for e in responses(n)))
            self.assertTrue(
                any(
                    e["file_name"] == "email.log"
                    for e in reports[n]
                    if "file_name" in e
                )
            )
        self.assertTrue(
            any(
                e.get("file_name") == "cache.json"
                and "FastAPI" in e["file_body"]
                for e in reports[17]
            )
        )
        self.assertTrue(
            any(
                e.get("file_name") == "sentiment.jsonl"
                and "positive" in e["file_body"]
                for e in reports[20]
            )
        )
        (ROOT / ".runtime" / "test-report.json").write_text(
            json.dumps(reports, indent=2), encoding="utf-8"
        )

    def test_studio_routes_and_subprocess_execution(self):
        import importlib
        # Explicit initialization survives tools that remove unused imports.
        importlib.import_module('app')
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.get("/").status_code, 200)
        self.assertEqual(len(client.get("/api/course").json()["lessons"]), 20)
        self.assertEqual(
            client.get(
                "/api/code/19", {"file": "routers/posts.py"}
            ).status_code,
            200,
        )
        for file in (".env", "../.env", "../../lesson28/.env", "unknown.py"):
            self.assertEqual(
                client.get("/api/code/19", {"file": file}).status_code, 404
            )
        self.assertEqual(
            client.post(
                "/api/run/6", "{}", content_type="application/json"
            ).status_code,
            403,
        )
        token = client.cookies["csrftoken"].value
        started = client.post(
            "/api/run/6",
            "{}",
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(started.status_code, 202)
        key = started.json()["id"]
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            job = client.get("/api/status/" + key).json()
            if job["status"] != "running":
                break
            time.sleep(0.05)
        self.assertEqual(job["status"], "done", job)
        self.assertTrue(any(e.get("http_status") == 204 for e in job["events"]))
        self.assertEqual(client.get("/api/docs/21").status_code, 404)


if __name__ == "__main__":
    unittest.main()
