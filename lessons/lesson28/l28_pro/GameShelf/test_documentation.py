import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase


class PolishDocumentationTests(SimpleTestCase):
    def test_generated_learning_documents_match_current_sources(self):
        lesson = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [sys.executable, str(lesson / "update_docs.py"), "--check"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
