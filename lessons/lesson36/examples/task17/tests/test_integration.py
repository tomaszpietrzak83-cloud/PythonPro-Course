import json
import tempfile
import unittest
from pathlib import Path

from deploy import deploy, rollback


class RollbackTest(unittest.TestCase):
    def test_rolls_back_failed_release(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            deploy(directory, "production", "v1")
            with self.assertRaises(RuntimeError):
                deploy(directory, "production", "v2", lambda _: False)
            rollback(directory)
            self.assertEqual(json.loads((directory / "production.json").read_text())["revision"], "v1")
