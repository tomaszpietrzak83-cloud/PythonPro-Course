"""ElevenLabs integration tests use a fake provider; no paid API calls."""

import json
import io
import os
import tempfile
import unittest
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

import app  # noqa: F401 - configure Django without starting a server
from django.test import Client
import eleven_narration as narration

CONFIG = {
    "key": "test-secret-never-return",
    "voice": "voice_test",
    "model": "eleven_multilingual_v2",
}


class ElevenTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.cache = Path(self.work.name)
        self.cache_patch = patch.object(narration, "CACHE", self.cache)
        self.cache_patch.start()
        self.addCleanup(self.cache_patch.stop)
        self.cfg = patch.object(narration, "config", return_value=CONFIG.copy())
        self.config_mock = self.cfg.start()
        self.addCleanup(self.cfg.stop)
        narration.VOICE_CACHE.clear()
        self.provider = patch.object(
            narration, "provider_request", side_effect=self.fake_provider
        )
        self.provider_mock = self.provider.start()
        self.addCleanup(self.provider.stop)

    def fake_provider(self, path, config, payload=None):
        if path.startswith("/v1/shared-voices"):
            return json.dumps(
                {
                    "voices": [
                        {
                            "voice_id": "polish_library",
                            "name": "Piotr - Engaging",
                            "language": "pl",
                            "free_users_allowed": True,
                        },
                        {
                            "voice_id": "english_library",
                            "name": "English",
                            "language": "en",
                            "free_users_allowed": True,
                        },
                        {
                            "voice_id": "premium_library",
                            "name": "Premium",
                            "language": "pl",
                            "free_users_allowed": False,
                        },
                    ]
                }
            ).encode()
        if path.startswith("/v2/voices"):
            return json.dumps(
                {
                    "voices": [
                        {
                            "voice_id": "voice_test",
                            "name": "Test voice",
                            "labels": {"language": "pl"},
                        }
                    ],
                    "has_more": False,
                }
            ).encode()
        self.assertEqual(
            payload["text"],
            json.loads(
                (narration.ROOT / "static/narrated-script.json").read_text(
                    encoding="utf-8"
                )
            )[0]["text"][0],
        )
        return b"ID3-test-mp3-bytes"

    def test_polish_list_includes_polish_library_and_excludes_english(self):
        result = narration.public_config("pl")
        self.assertEqual(
            {v["id"] for v in result["voices"]}, {"voice_test", "polish_library"}
        )
        self.assertTrue(all(v["language"] == "pl" for v in result["voices"]))
        self.assertNotIn("english_library", {v["id"] for v in result["voices"]})
        self.assertNotIn("premium_library", {v["id"] for v in result["voices"]})

    def test_same_clip_generates_once_even_concurrently(self):
        with ThreadPoolExecutor(2) as pool:
            results = list(
                pool.map(lambda _: narration.generate("pl", 0, "voice_test"), range(2))
            )
        self.assertEqual(results[0]["url"], results[1]["url"])
        self.assertEqual(sum(not r["cached"] for r in results), 1)
        calls = [
            c
            for c in self.provider_mock.call_args_list
            if c.args[0].startswith("/v1/text-to-speech/")
        ]
        self.assertEqual(len(calls), 1)

    def test_cached_mp3_plays_without_key_or_provider(self):
        first = narration.generate("pl", 0, "voice_test")
        self.config_mock.return_value = dict(CONFIG, key="")
        self.provider_mock.reset_mock()
        again = narration.generate("pl", 0, "voice_test")
        self.assertTrue(again["cached"])
        self.assertEqual(again["url"], first["url"])
        self.provider_mock.assert_not_called()
        self.assertTrue(narration.public_config()["cached_available"])

    def test_config_never_contains_api_key(self):
        response = Client().get("/api/narration/config")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(CONFIG["key"], response.content.decode())
        self.assertEqual(response.json()["voices"][0]["id"], "voice_test")

    def test_generation_and_audio_with_real_csrf(self):
        client = Client(enforce_csrf_checks=True)
        data = {"language": "pl", "step": 0, "voice_id": "voice_test"}
        self.assertEqual(
            client.post(
                "/api/narration/generate", data, content_type="application/json"
            ).status_code,
            403,
        )
        client.get("/")
        response = client.post(
            "/api/narration/generate",
            data,
            content_type="application/json",
            HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value,
        )
        self.assertEqual(response.status_code, 200)
        recording = client.get(response.json()["url"])
        try:
            self.assertEqual(recording["Content-Type"], "audio/mpeg")
            self.assertEqual(
                b"".join(recording.streaming_content), b"ID3-test-mp3-bytes"
            )
        finally:
            recording.close()

    def test_user_cannot_supply_arbitrary_paid_text_or_path(self):
        client = Client()
        data = {"language": "pl", "step": 0, "voice_id": "voice_test"}
        response = client.post(
            "/api/narration/generate",
            dict(data, text="arbitrary"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        for invalid in (
            dict(data, step=True),
            dict(data, step=12),
            dict(data, language="xx"),
            dict(data, voice_id="../bad"),
        ):
            response = client.post(
                "/api/narration/generate", invalid, content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)
        self.assertEqual(client.get("/api/narration/audio/not-a-hash").status_code, 404)
        self.provider_mock.assert_not_called()

    def test_missing_key_is_a_setup_message_not_traceback(self):
        self.config_mock.return_value = dict(CONFIG, key="")
        result = Client().get("/api/narration/config").json()
        self.assertFalse(result["configured"])
        response = Client().post(
            "/api/narration/generate",
            {"language": "pl", "step": 0, "voice_id": "voice_test"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 503)
        self.assertIn("ELEVENLABS_API_KEY", response.json()["error"])


class ProviderTests(unittest.TestCase):
    def test_activity_block_is_not_reported_as_a_bad_key(self):
        body = io.BytesIO(
            json.dumps(
                {
                    "detail": {
                        "status": "detected_unusual_activity",
                        "message": CONFIG["key"],
                    }
                }
            ).encode()
        )
        error = urllib.error.HTTPError(
            "https://api.elevenlabs.io", 401, "Unauthorized", {}, body
        )
        with patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaises(narration.NarrationError) as caught:
                narration.provider_request("/v2/voices", CONFIG)
        self.assertIn("detected_unusual_activity", str(caught.exception))
        self.assertNotIn(CONFIG["key"], str(caught.exception))

    def test_local_env_changes_do_not_require_a_restart(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work) / "lessons" / "lesson34"
            root.mkdir(parents=True)
            with (
                patch.object(narration, "ROOT", root),
                patch.dict(os.environ, {}, clear=True),
            ):
                (root / ".env").write_text(
                    "ELEVENLABS_API_KEY=test-one\n", encoding="utf-8"
                )
                self.assertEqual(narration.config()["key"], "test-one")
                (root / ".env").write_text(
                    "ELEVENLABS_API_KEY=test-two\n", encoding="utf-8"
                )
                self.assertEqual(narration.config()["key"], "test-two")

    def test_errors_do_not_expose_provider_body_or_key(self):
        error = urllib.error.HTTPError(
            "https://api.elevenlabs.io", 401, "Unauthorized", {}, None
        )
        with patch("urllib.request.urlopen", side_effect=error):
            with self.assertRaises(narration.NarrationError) as caught:
                narration.provider_request("/v2/voices", CONFIG)
        self.assertNotIn(CONFIG["key"], str(caught.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
