"""Source mapping, endpoint validation, real worker and comparison checks."""
import ast
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import app
from curriculum import STEPS, lesson, source_steps
from django.test import Client


class TeachingTests(unittest.TestCase):
    def test_assignment_before_introduction_for_all_tasks(self):
        from assignments import assignment, english_code
        for number in range(1, 21):
            data = assignment(number)
            self.assertTrue(data["pages"]["pl"])
            self.assertTrue(data["pages"]["en"])
            for language in ("pl", "en"):
                for page in data["pages"][language]:
                    for block in page:
                        if block["kind"] == "code":
                            self.assertEqual(block["text"], english_code(block["text"]))
            self.assertEqual(lesson(number)["assignment"], data)
        first = " ".join(b.get("text", "") + " ".join(b.get("items", [])) for page in assignment(1)["pages"]["pl"] for b in page)
        self.assertIn("3 sekundy", first)
        self.assertIn("The worker thread has finished!", first)
        self.assertIn("The main program is waiting for the thread...", first)
        self.assertIn("input()", assignment(8)["adaptation"]["pl"])

    def test_examples_use_english_code(self):
        for path in (ROOT / "examples").glob("*.py"):
            source = path.read_text(encoding="utf-8")
            self.assertFalse(set(source) & set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"), path.name)
        bank = ast.parse((ROOT / "examples" / "task18.py").read_text(encoding="utf-8"))
        self.assertEqual([node.name for node in bank.body if isinstance(node, ast.ClassDef)], ["BankAccount"])

    def test_first_thread_start_is_same_snapshot_line_18(self):
        response = Client().get("/api/course")
        self.assertEqual(response["Cache-Control"], "no-store")
        data = response.json()["lessons"][0]["steps"]
        start = next(s for s in data["steps"] if s["id"] == "start")
        self.assertEqual((start["start"], start["end"]), (18, 18))
        self.assertEqual(data["source"].splitlines()[17].strip(), "worker_thread.start()")
        self.assertIn("start", data["rows"][17])
        self.assertNotIn("start", data["rows"][15])
        self.assertEqual(len(data["rows"]), len(data["source"].splitlines()))

    def test_review_rejects_semantic_drift_without_line_changes(self):
        original = Path.read_text

        def changed(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            return text.replace("time.sleep(3)", "time.sleep(4)") if path.name == "task01.py" else text

        with patch.object(Path, "read_text", changed):
            with self.assertRaisesRegex(ValueError, "Comment needs review"):
                source_steps(1)

    def test_no_instruction_is_explained_twice_by_different_blocks(self):
        for number in range(1, 21):
            seen = set()
            for block in source_steps(number)["steps"]:
                for detail in block["details"]:
                    key = (detail["start"], detail["end"])
                    self.assertNotIn(key, seen, f"Task {number}, block {block['id']}")
                    seen.add(key)

    def test_hashing_and_reconciliation_describe_highlighted_operations(self):
        data = source_steps(16)
        blocks = {s["id"]: s for s in data["steps"]}
        rows = data["source"].splitlines()
        selected = "\n".join(rows[blocks["hash"]["start"]-1:blocks["hash"]["end"]])
        self.assertIn("iter(lambda:", selected)
        self.assertIn("digest.update(chunk)", selected)
        reconciliation = source_steps(18)
        block = next(s for s in reconciliation["steps"] if s["id"] == "reconcile")
        self.assertIn("200 + sum(account.history)", reconciliation["source"].splitlines()[block["start"]-1])

    def test_all_markers_resolve_to_exact_statements(self):
        for number in range(1, 21):
            with self.subTest(number=number):
                data = source_steps(number)
                tree = ast.parse(data["source"])
                statements = {(n.lineno, n.end_lineno) for n in ast.walk(tree)
                              if isinstance(n, ast.stmt)}
                self.assertEqual({s["id"] for s in data["steps"]}, set(STEPS[number]))
                for step in data["steps"]:
                    self.assertIn((step["start"], step["end"]), statements)
                    marker = data["source"].splitlines()[step["start"] - 2]
                    self.assertEqual(marker.strip(), f"# @step {step['id']}")
                    for detail in step["details"]:
                        self.assertLessEqual(step["start"], detail["start"])
                        self.assertLessEqual(detail["start"], detail["end"])
                        self.assertLessEqual(detail["end"], step["end"])
                        self.assertEqual(set(detail["body"]), {"pl", "en"})

    def test_source_display_matches_real_file(self):
        client = Client()
        for number in range(1, 21):
            data = client.get(f"/api/code/{number}").json()
            source = (ROOT / "examples" / f"task{number:02}.py").read_text(encoding="utf-8")
            self.assertEqual(data["source"], source)
            self.assertEqual(len(data["rows"]), len(source.splitlines()))

    def test_curriculum_and_presets(self):
        client = Client()
        self.assertEqual(client.get("/").status_code, 200)
        items = client.get("/api/course").json()["lessons"]
        self.assertEqual(len(items), 20)
        self.assertEqual(len({x["intro"]["pl"] for x in items}), 20)
        for item in items:
            for preset in item["presets"]:
                app.validate(item["number"], preset["value"])

    def test_validation_and_csrf(self):
        for number, data in [(12, {"size": 0}), (19, {"workers": 100}),
                             (20, {"side": 1001}), (17, {"numbers": []}),
                             (17, {"numbers": [float("nan")]}),
                             (8, {"name": ""}), (1, {"command": "bad"})]:
            with self.subTest(number=number):
                with self.assertRaises(ValueError):
                    app.validate(number, data)
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post("/api/run/1", data="{}", content_type="application/json").status_code, 403)
        self.assertEqual(client.get("/api/run/1").status_code, 405)
        self.assertEqual(client.get("/api/code/99").status_code, 404)


class RealExecutionTests(unittest.TestCase):
    def run_example(self, number, inputs=None):
        env = dict(os.environ, PYTHONIOENCODING="utf-8", LESSON30_INPUT=json.dumps(inputs or {}))
        result = subprocess.run([sys.executable, "-u", str(ROOT / "examples" / f"task{number:02}.py")],
                                env=env, capture_output=True, text=True, encoding="utf-8", timeout=100)
        self.assertEqual(result.returncode, 0, result.stderr)
        events = [json.loads(row) for row in result.stdout.splitlines()]
        self.assertFalse(any(e["kind"] == "error" for e in events), events)
        self.assertEqual(events[0]["kind"], "boot")
        self.assertEqual(events[-1]["kind"], "done")
        return events

    def test_every_default_example_and_observable_results(self):
        report = {}
        for number in range(1, 21):
            with self.subTest(number=number):
                events = self.run_example(number, lesson(number)["presets"][0]["value"])
                metrics = {e["label"]: e["value"] for e in events if e["kind"] == "metric"}
                report[number] = metrics
                if number == 3:
                    self.assertGreater(metrics["Sequential"], 5.8)
                    self.assertLess(metrics["Threads"], metrics["Sequential"] * .7)
                if number in (4, 5):
                    self.assertEqual(metrics["List length"], 200_000)
                    self.assertEqual(metrics["Counter (expected: 2)"], 1 if number == 4 else 2)
                if number == 6:
                    self.assertTrue(any("3628800" in e["label"] for e in events))
                    self.assertGreaterEqual(len({e["pid"] for e in events}), 2)
                if number == 9:
                    self.assertEqual(metrics["Sum"], metrics["Expected sum"])
                if number == 10:
                    self.assertEqual(metrics["Total"], 4)
                if number == 12:
                    sums = [e["label"] for e in events if e["label"].startswith("Sum:")]
                    self.assertEqual(len(sums), 6)
                    self.assertEqual(len(set(sums)), 1)
                if number == 13:
                    self.assertEqual(metrics["Prime numbers"], 12)
                if number == 14:
                    self.assertTrue(metrics["Copies match"])
                    self.assertEqual(metrics["Copied files"], 4)
                if number == 15:
                    self.assertEqual(metrics["Unique pages"], 4)
                    self.assertEqual(len([e for e in events if e["kind"] == "start"]), 4)
                if number == 16:
                    self.assertEqual(metrics["Hashes"], 4)
                if number == 17:
                    self.assertEqual(metrics["Sum"], 20)
                    self.assertEqual(metrics["Mean"], 5)
                if number == 18:
                    self.assertEqual(metrics["Balance"], metrics["Reconciled balance"])
                if number == 19:
                    self.assertEqual(metrics["Analyzed reviews"], 20)
                if number == 20:
                    self.assertTrue(metrics["Identical results"])
                    self.assertEqual(metrics["Processed pixels"], 900_000)
        (ROOT / ".runtime").mkdir(exist_ok=True)
        (ROOT / ".runtime" / "verification.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    unittest.main(verbosity=2)
