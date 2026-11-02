"""Run a real Uvicorn server, exercise HTTP endpoints, and retain evidence files."""

import argparse
import asyncio
import importlib
import json
import os
import socket
import sys
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
import uvicorn
from lab_support import event, launch, metric, span

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scenarios import scenarios


def check_subset(actual, expected):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and check_subset(actual[key], value)
            for key, value in expected.items()
        )
    return actual == expected


@asynccontextmanager
async def serve(app):
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    config = uvicorn.Config(
        app, log_level="critical", access_log=False, lifespan="on"
    )
    server = uvicorn.Server(config)
    task = asyncio.create_task(server.serve(sockets=[sock]))
    try:
        async with asyncio.timeout(10):
            while not server.started:
                if task.done():
                    await task
                    raise RuntimeError(
                        "API failed during startup; check PostgreSQL and configuration"
                    )
                await asyncio.sleep(0.01)
        yield f"http://127.0.0.1:{sock.getsockname()[1]}"
    finally:
        server.should_exit = True
        try:
            await asyncio.wait_for(task, 10)
        finally:
            sock.close()


async def request(client, url, case):
    method, path = case["method"], case["path"]
    with span(method + " " + path, "HTTP request"):
        event(
            "log",
            "client",
            f"{method} {path}",
            http_method=method,
            http_url=url + path,
            request_body=case["data"],
        )
        response = await client.request(
            method, url + path, json=case["data"], headers=case["headers"]
        )
        body = response.text
        event(
            "log",
            "response",
            f"{response.status_code}: {body[:1500]}",
            http_method=method,
            http_url=url + path,
            http_status=response.status_code,
            response_body=body,
            content_type=response.headers.get("content-type", ""),
            response_headers={
                k: v
                for k, v in response.headers.items()
                if k.lower() in {"x-request-id", "content-type"}
            },
        )
        assert response.status_code == case["status"], (
            f"{method} {path}: expected {case['status']}, received {response.status_code}: {body}"
        )
        if case["expected"] is not None:
            assert check_subset(response.json(), case["expected"]), (
                f"Unexpected response: {body}"
            )
        if path == "/random":
            assert 1 <= response.json()["number"] <= 100
        if path == "/openapi.json":
            assert response.json()["info"]["title"] == "Book Workshop"
        if "X-Request-ID" in response.headers:
            metric("X-Request-ID", response.headers["X-Request-ID"])
        metric("HTTP status", response.status_code)
        return response


async def run(number, app, folder):
    if number == 17:
        (folder / "cache.json").write_text(
            '{"source":"startup-file"}', encoding="utf-8"
        )
    async with serve(app) as url:
        async with httpx.AsyncClient(timeout=15) as client:
            for case in scenarios(number):
                await request(client, url, case)
            # BackgroundTasks execute after the response; wait for actual evidence,
            # rather than assuming that receiving a response means all work is done.
            expected_files = {
                15: ["notifications.log", "stats.json"],
                19: ["email.log"],
                20: ["email.log", "sentiment.jsonl"],
            }.get(number, [])
            async with asyncio.timeout(5):
                while not all(
                    (folder / name).exists() for name in expected_files
                ):
                    await asyncio.sleep(0.01)
    files = []
    for path in folder.iterdir():
        if path.is_file():
            body = path.read_text(encoding="utf-8")
            event(
                "log",
                "file",
                f"{path.name}: {body}",
                file_name=path.name,
                file_body=body,
            )
            files.append(path.name)
    if number == 15:
        assert json.loads((folder / "stats.json").read_text()) == {"books": 0}
    if number == 16:
        records = [
            json.loads(line)
            for line in (folder / "requests.log").read_text().splitlines()
        ]
        assert len(records) == 2 and all(row["request_id"] for row in records)
    if number == 17:
        assert (
            json.loads((folder / "cache.json").read_text())["topic"]
            == "FastAPI"
        )
    if number == 20:
        assert (
            json.loads(
                (folder / "sentiment.jsonl").read_text().splitlines()[0]
            )["sentiment"]
            == "positive"
        )
    metric("Verified HTTP cases", len(scenarios(number)))
    if files:
        metric("Evidence files", ", ".join(files))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, choices=range(1, 21))
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8133)
    args = parser.parse_args()
    task_folder = ROOT / "examples" / f"task{args.number:02}"
    sys.path.insert(0, str(task_folder))
    runtime = ROOT / ".runtime"
    runtime.mkdir(exist_ok=True)
    folder = Path(
        tempfile.mkdtemp(prefix=f"task{args.number:02}-", dir=runtime)
    )
    os.environ["LESSON33_WORKDIR"] = str(folder)
    app = importlib.import_module("main").app
    if args.serve:
        uvicorn.run(app, host="127.0.0.1", port=args.port, access_log=False)
    else:
        launch(lambda options: asyncio.run(run(args.number, app, folder)))


if __name__ == "__main__":
    main()
