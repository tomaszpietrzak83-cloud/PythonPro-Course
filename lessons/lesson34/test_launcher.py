"""Regression coverage for Windows PID reuse and denied process access."""

import json
import unittest
from unittest.mock import Mock, patch

import psutil
import run_app


class LauncherTests(unittest.TestCase):
    def record(self):
        return Mock(
            read_text=Mock(return_value=json.dumps({"pid": 9096, "created": 100}))
        )

    @patch("psutil.Process")
    def test_reused_pid_never_reads_command_or_terminates(self, factory):
        process = factory.return_value
        process.create_time.return_value = 200
        process.cmdline.side_effect = psutil.AccessDenied(9096)
        run_app.stop_previous(self.record())
        process.cmdline.assert_not_called()
        process.terminate.assert_not_called()

    @patch("psutil.Process")
    def test_access_denied_is_handled_without_termination(self, factory):
        process = factory.return_value
        process.create_time.return_value = 100
        process.cmdline.side_effect = psutil.AccessDenied(9096)
        with patch("builtins.print"):
            run_app.stop_previous(self.record())
        process.terminate.assert_not_called()

    @patch("psutil.Process")
    def test_unrelated_command_is_not_terminated(self, factory):
        process = factory.return_value
        process.create_time.return_value = 100
        process.cmdline.return_value = ["another-app.py"]
        run_app.stop_previous(self.record())
        process.terminate.assert_not_called()

    @patch("psutil.wait_procs", return_value=([], []))
    @patch("psutil.Process")
    def test_verified_lesson_process_is_stopped(self, factory, wait):
        process = factory.return_value
        process.create_time.return_value = 100
        process.cmdline.return_value = ["python", str(run_app.ROOT / "app.py")]
        process.children.return_value = []
        run_app.stop_previous(self.record())
        process.terminate.assert_called_once()

    def test_broken_record_is_ignored(self):
        with patch("builtins.print"):
            run_app.stop_previous(Mock(read_text=Mock(return_value="{")))


if __name__ == "__main__":
    unittest.main()
