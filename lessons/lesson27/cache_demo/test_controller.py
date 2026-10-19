"""Verify process ownership and the local controller's mutation boundary."""

import json
import re
import socket
import threading
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from cache_demo.controller import ProcessManager, create_controller


class ProcessOwnershipTests(unittest.TestCase):
    def test_stop_does_not_touch_unowned_processes(self):
        manager = ProcessManager(lambda project: {}, lambda port: False)
        manager.stop("l27_pro")
        self.assertFalse(manager.state()["l27_pro"]["running"])
        with patch("cache_demo.controller.subprocess.Popen") as launch:
            with self.assertRaisesRegex(RuntimeError, "occupied"):
                manager.start("l27_pro")
            launch.assert_not_called()

    def test_owned_process_is_terminated_and_waited_for(self):
        manager = ProcessManager(lambda project: {}, lambda port: True)
        child = Mock()
        child.poll.return_value = None
        manager.children["l27_pro"] = child
        manager.stop("l27_pro")
        child.terminate.assert_called_once()
        child.wait.assert_called_once_with(timeout=5)


class ControllerHttpTests(unittest.TestCase):
    def test_valid_token_and_origin_are_required_for_process_actions(self):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        manager = Mock()
        manager.state.return_value = {"l27_pro": {"running": False, "pid": None, "port": 8000}}
        with patch("cache_demo.controller.CONTROL_PORT", port):
            server = create_controller(manager)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            base = f"http://127.0.0.1:{port}"
            try:
                with urlopen(base + "/") as response:
                    html = response.read().decode()
                    self.assertEqual(response.headers["X-Lesson27-Controller"], "CacheLab")
                boot = json.loads(re.search(r'<script id="demo-boot"[^>]*>(.*?)</script>', html, re.S).group(1))
                body = json.dumps({"action": "start"}).encode()
                for headers in ({"Origin": base}, {"Origin": "https://unrelated.example", "X-Control-Token": boot["control_token"]}):
                    with self.assertRaises(HTTPError) as error:
                        urlopen(Request(base + "/control/l27_pro/", data=body, headers=headers))
                    self.assertEqual(error.exception.code, 403)
                manager.start.assert_not_called()
                request = Request(base + "/control/l27_pro/", data=body,
                                  headers={"Origin": base, "X-Control-Token": boot["control_token"]})
                with urlopen(request) as response:
                    self.assertEqual(response.status, 200)
                manager.start.assert_called_once_with("l27_pro")
                # Static paths cannot traverse into source files or databases.
                with self.assertRaises(HTTPError) as error:
                    urlopen(base + "/static/cache_demo/../../controller.py")
                self.assertEqual(error.exception.code, 404)
            finally:
                server.shutdown()
                server.server_close()
                worker.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
