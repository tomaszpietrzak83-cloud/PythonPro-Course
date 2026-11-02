"""Integration checks: real sockets, HTTP, database and annotation/source alignment.

Run with the lesson's Python: python test_lesson34.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "examples"))
from aiohttp import ClientSession
import jwt
from run_task import Wire, game_round, server, token
from curriculum import lesson


def module(number):
    spec = importlib.util.spec_from_file_location(
        f"task{number:02}_tested", ROOT / "examples" / f"task{number:02}" / "main.py"
    )
    result = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = result
    spec.loader.exec_module(result)
    return result


class NetworkTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.work = tempfile.TemporaryDirectory(dir=ROOT / ".runtime")
        self.old_work = os.environ.get("LESSON34_WORKDIR")
        os.environ["LESSON34_WORKDIR"] = self.work.name
        self.session = ClientSession()
        self.output = patch("run_task.event")
        self.output.__enter__()

    async def asyncTearDown(self):
        await self.session.close()
        self.output.__exit__(None, None, None)
        if self.old_work is None:
            os.environ.pop("LESSON34_WORKDIR", None)
        else:
            os.environ["LESSON34_WORKDIR"] = self.old_work
        self.work.cleanup()

    async def test_game_draw_and_disconnect(self):
        for moves, disconnected, expected in [
            ([0, 1, 2, 4, 3, 5, 7, 6, 8], False, "draw"),
            ([], True, "disconnected"),
        ]:
            game_module = module(20)
            game_module_app = game_module.create_app()
            async with server(game_module_app) as url:
                state = await game_round(
                    Wire(self.session, url), moves, disconnect=disconnected
                )
                self.assertEqual(state["status"], expected)
            self.assertFalse(game_module_app["game"].players)

    async def test_game_invalid_and_occupied_cells_preserve_state(self):
        game = module(20).Game()
        game.status = "playing"
        for invalid in [-1, 9, True, "0", None]:
            before = game.snapshot().copy()
            before["board"] = game.board.copy()
            self.assertIsNotNone(game.move("X", invalid))
            self.assertEqual(game.snapshot(), before)
        self.assertIsNone(game.move("X", 0))
        self.assertIsNotNone(game.move("O", 0))
        self.assertEqual(game.turn, "O")

    async def test_sqlite_latest_50_and_restart(self):
        task = module(16)
        async with server(task.create_app()) as url:
            wire = Wire(self.session, url)
            ws = await wire.connect()
            await wire.send(ws, "Anna")
            await wire.receive(ws)
            for i in range(55):
                await wire.send(ws, f"message-{i}")
                await wire.receive(ws)
            await ws.close()
        # Reopen the SAME SQLite file through a new server/module.
        task = module(16)
        async with server(task.create_app()) as url:
            wire = Wire(self.session, url)
            ws = await wire.connect()
            await wire.send(ws, "Jan")
            history = (await wire.receive(ws))["messages"]
            self.assertEqual(
                [r["body"] for r in history], [f"message-{i}" for i in range(5, 55)]
            )
            self.assertTrue(
                all(
                    r["nickname"] == "Anna" and r["sent_at"].endswith("+00:00")
                    for r in history
                )
            )
            await ws.close()
        self.assertFalse(task.clients)

    async def test_jwt_wrong_algorithm_and_unknown_identity(self):
        task = module(14)
        async with server(task.create_app()) as url:
            wire = Wire(self.session, url)
            bad_tokens = [
                jwt.encode(
                    {"sub": "1", "exp": 9999999999}, task.DEMO_SECRET, algorithm="HS384"
                ),
                token(task, "99"),
                jwt.encode({"sub": "1"}, task.DEMO_SECRET, algorithm="HS256"),
            ]
            for value in bad_tokens:
                ws = await wire.connect()
                await wire.send(ws, value, redact=True)
                self.assertEqual((await wire.receive(ws))["code"], 1008)
                await ws.close()

    async def test_dataloader_is_request_scoped(self):
        task = module(17)
        async with server(task.create_app()) as url:
            wire = Wire(self.session, url)
            first = await wire.graphql("{ users { posts } }")
            self.assertEqual(task.fetch_count, 1)
            second = await wire.graphql("{ users { posts } }")
            self.assertEqual(first, second)
            self.assertEqual(task.fetch_count, 2)


class MaterialTests(unittest.TestCase):
    def test_every_note_and_row_matches_current_source(self):
        for number in range(1, 21):
            record = lesson(number)
            self.assertTrue(record["forecast"]["pl"])
            self.assertTrue(record["assignment"]["pages"]["pl"])
            for file, data in record["steps"]["sources"].items():
                self.assertEqual(
                    data["source"],
                    (ROOT / "examples" / f"task{number:02}" / file).read_text(
                        encoding="utf-8"
                    ),
                )
                self.assertEqual(
                    len(data["annotated_rows"]), len(data["source"].splitlines())
                )
                for row in data["annotated_rows"]:
                    self.assertEqual(
                        data["notes"][row["line_note"]]["start"], row["line"]
                    )
                    self.assertIn(row["block_note"], data["notes"])
                for note in data["notes"].values():
                    self.assertLessEqual(1, note["start"])
                    self.assertLessEqual(note["end"], len(data["annotated_rows"]))
                    self.assertTrue(note["body"]["pl"])
                    self.assertTrue(note["body"]["en"])

    def test_all_twenty_real_demonstrations(self):
        for number in range(1, 21):
            with self.subTest(task=number):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "examples" / "run_task.py"),
                        str(number),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    timeout=20,
                )
                self.assertEqual(
                    result.returncode, 0, result.stdout[-4000:] + result.stderr[-2000:]
                )
                events = [json.loads(line) for line in result.stdout.splitlines()]
                self.assertTrue(
                    any(
                        e.get("label") == "Scenario verified" and e.get("value") is True
                        for e in events
                    )
                )


if __name__ == "__main__":
    (ROOT / ".runtime").mkdir(exist_ok=True)
    unittest.main(verbosity=2)
