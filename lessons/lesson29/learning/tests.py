from types import SimpleNamespace
from unittest.mock import patch

from django.test import Client, SimpleTestCase, TestCase


class TaskEndpointTests(SimpleTestCase):
    def test_get_does_not_enqueue_work(self):
        with patch("learning.views.hello_world.delay") as publish:
            self.assertEqual(self.client.get("/tasks/1/run/").status_code, 405)
            publish.assert_not_called()

    def test_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        with patch("learning.views.hello_world.delay") as publish:
            self.assertEqual(client.post("/tasks/1/run/").status_code, 403)
            publish.assert_not_called()

    def test_broker_error_is_reported_without_exposing_details(self):
        with patch(
            "learning.views.hello_world.delay",
            side_effect=ConnectionError("private connection details"),
        ):
            response = self.client.post("/tasks/1/run/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"error": "broker_unavailable"})


class MultiplyEndpointTests(SimpleTestCase):
    def test_invalid_inputs_never_enter_the_queue(self):
        for data in (
            {},
            {"a": "abc", "b": "2"},
            {"a": "nan", "b": "3"},
            {"a": "inf", "b": "2"},
            {"a": "1e13", "b": "1"},
        ):
            with (
                self.subTest(data=data),
                patch("learning.views.multiply.delay") as publish,
            ):
                self.assertEqual(
                    self.client.post("/tasks/2/run/", data).status_code, 400
                )
                publish.assert_not_called()

    def test_form_numbers_are_published_as_numbers(self):
        with patch(
            "learning.views.multiply.delay",
            return_value=SimpleNamespace(id="sample-id"),
        ) as publish:
            response = self.client.post(
                "/tasks/2/run/", {"a": "0", "b": "-2.5"}
            )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()["task_id"], "sample-id")
        publish.assert_called_once_with(0.0, -2.5)

    def test_submission_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        with patch("learning.views.multiply.delay") as publish:
            self.assertEqual(
                client.post("/tasks/2/run/", {"a": "1", "b": "2"}).status_code,
                403,
            )
            publish.assert_not_called()

    def test_unimplemented_task_is_not_a_working_lesson(self):
        self.assertEqual(self.client.get("/tasks/21/").status_code, 404)


class ExtendedLessonTests(TestCase):
    def test_every_lesson_has_material_and_live_code_anchors(self):

        from django.conf import settings

        from learning.curriculum import get_curriculum

        files = [
            "learning/tasks.py",
            "learning/views.py",
            "academy/celery.py",
            "academy/urls.py",
            "academy/settings.py",
            "learning/models.py",
            "learning/management/commands/enqueue_tasks.py",
            "run_app.py",
        ]
        for number in range(3, 21):
            with self.subTest(number=number):
                material = get_curriculum(number)
                self.assertGreaterEqual(len(material["questions"]), 2)
                for step in material["steps"]:
                    self.assertIn(
                        step["needle"],
                        (settings.BASE_DIR / files[step["file"]]).read_text(
                            encoding="utf-8"
                        ),
                    )
                self.assertEqual(
                    self.client.get(f"/tasks/{number}/").status_code, 200
                )

    def test_retention_preserves_recent_and_boundary_records(self):
        from datetime import timedelta

        from django.utils import timezone

        from learning.models import LogEntry
        from learning.tasks import clean_logs

        now = timezone.now()
        old = LogEntry.objects.create(
            message="old", created_at=now - timedelta(days=91)
        )
        boundary = LogEntry.objects.create(
            message="boundary", created_at=now - timedelta(days=90)
        )
        recent = LogEntry.objects.create(
            message="recent", created_at=now - timedelta(days=1)
        )
        with patch("learning.tasks.timezone.now", return_value=now):
            self.assertEqual(clean_logs()["deleted"], 1)
        self.assertFalse(LogEntry.objects.filter(pk=old.pk).exists())
        self.assertTrue(
            LogEntry.objects.filter(pk__in=[boundary.pk, recent.pk]).count()
            == 2
        )

    def test_commit_publishes_after_record_is_saved(self):
        from learning.models import ProcessingRecord

        with patch(
            "learning.views.tasks.process_record.apply_async"
        ) as publish:
            with self.captureOnCommitCallbacks(execute=True) as callbacks:
                response = self.client.post("/tasks/20/run/", {"text": "test"})
                publish.assert_not_called()
            self.assertEqual(response.status_code, 202)
            self.assertEqual(len(callbacks), 1)
            publish.assert_called_once_with(
                args=[ProcessingRecord.objects.get().pk],
                task_id=response.json()["task_id"],
            )

    def test_rollback_discards_record_and_publication(self):
        from learning.models import ProcessingRecord

        with patch(
            "learning.views.tasks.process_record.apply_async"
        ) as publish:
            with self.captureOnCommitCallbacks(execute=True) as callbacks:
                response = self.client.post(
                    "/tasks/20/run/", {"text": "discard", "rollback": "yes"}
                )
            self.assertEqual(response.json()["state"], "ROLLED_BACK")
            self.assertEqual(callbacks, [])
            self.assertEqual(ProcessingRecord.objects.count(), 0)
            publish.assert_not_called()

    def test_invalid_image_is_not_saved_or_queued(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from learning.models import UploadedImage

        with patch("learning.views.tasks.classify_image.delay") as publish:
            response = self.client.post(
                "/tasks/16/run/",
                {"image": SimpleUploadedFile("bad.png", b"not an image")},
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(UploadedImage.objects.count(), 0)
        publish.assert_not_called()

    def test_retry_uses_required_countdown_and_limit(self):
        import requests

        from learning.tasks import retry_connection

        with (
            patch(
                "learning.tasks.requests.get",
                side_effect=requests.ConnectionError("offline"),
            ),
            patch.object(
                retry_connection, "retry", side_effect=RuntimeError("retry")
            ) as retry,
        ):
            with self.assertRaises(RuntimeError):
                retry_connection()
            self.assertEqual(retry.call_args.kwargs["countdown"], 60)
            self.assertEqual(retry.call_args.kwargs["max_retries"], 3)


class SlideSelectionTests(SimpleTestCase):
    def test_all_slide_fragments_resolve_inside_their_declared_scope(self):
        import re

        from django.conf import settings

        from learning.code_ranges import code_ranges
        from learning.curriculum import get_curriculum

        files = [
            "learning/tasks.py",
            "learning/views.py",
            "academy/celery.py",
            "academy/urls.py",
            "academy/settings.py",
            "learning/models.py",
            "learning/management/commands/enqueue_tasks.py",
            "run_app.py",
        ]
        parsed = [
            code_ranges((settings.BASE_DIR / name).read_text(encoding="utf-8"))
            for name in files
        ]
        for number in range(3, 21):
            for step in get_curriculum(number)["steps"]:
                for needle in [step["needle"], *step.get("also", [])]:
                    with self.subTest(task=number, needle=needle):
                        ranges = parsed[step["file"]]
                        if step.get("context"):
                            context = re.sub(r"\s+", "", step["context"])
                            scope = next(
                                r
                                for r in ranges
                                if r["text"].startswith(context)
                            )
                            ranges = [
                                r
                                for r in ranges
                                if r["start"] >= scope["start"]
                                and r["end"] <= scope["end"]
                            ]
                        compact = re.sub(r"\s+", "", needle)
                        matches = [
                            r for r in ranges if r["text"].startswith(compact)
                        ]
                        if not matches:
                            matches = [
                                r for r in ranges if compact in r["text"]
                            ]
                        self.assertTrue(
                            matches, "Slide fragment cannot be highlighted"
                        )

    def test_scraping_has_separate_network_parser_database_and_schedule_slides(
        self,
    ):
        from learning.curriculum import get_curriculum

        steps = get_curriculum(13)["steps"]
        by_needle = {s["needle"]: s for s in steps}
        self.assertIn(
            "timeout=15", by_needle["response = requests.get"]["pl"][2]
        )
        self.assertIn("get_text", by_needle["title = BeautifulSoup"]["en"][1])
        self.assertIn(
            "objects.create",
            by_needle["page = ScrapedPage.objects.create"]["pl"][1],
        )
        self.assertIn(
            "crontab(minute=0)", by_needle['"hourly-page-title"']["pl"][1]
        )
