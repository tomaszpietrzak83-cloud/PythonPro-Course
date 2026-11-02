"""Real aiohttp/GraphQL/WebSocket demonstrations with recorded network evidence."""

import argparse
import asyncio
import importlib
import json
import os
import sys
import tempfile
import warnings
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from aiohttp import ClientSession, ClientTimeout, WSMsgType, web
from aiohttp.web_exceptions import NotAppKeyWarning
from lab_support import event, launch, metric, span

ROOT = Path(__file__).resolve().parents[1]
warnings.filterwarnings("ignore", category=NotAppKeyWarning)


@asynccontextmanager
async def server(app):
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        host, port = runner.addresses[0]
        yield f"http://{host}:{port}"
    finally:
        await runner.cleanup()


class Wire:
    def __init__(self, session, url):
        self.session, self.url = session, url

    async def connect(self, name="client", protocols=()):
        ws = await self.session.ws_connect(
            self.url.replace("http://", "ws://")
            + ("/graphql" if protocols else "/ws"),
            protocols=protocols,
        )
        event(
            "log",
            name,
            "WebSocket connected; HTTP upgrade accepted",
            ws_client=name,
            ws_direction="connect",
            ws_body="Handshake complete",
        )
        return ws

    async def send(self, ws, value, name="client", redact=False):
        if isinstance(value, str):
            await ws.send_str(value)
        else:
            await ws.send_json(value)
        event(
            "log",
            name,
            "Client → server",
            ws_client=name,
            ws_direction="send",
            ws_body="[signed demo JWT]" if redact else value,
        )

    async def receive(self, ws, name="client"):
        message = await asyncio.wait_for(ws.receive(), 3)
        if message.type == WSMsgType.TEXT:
            try:
                value = json.loads(message.data)
            except ValueError:
                value = message.data
        elif message.type in (WSMsgType.CLOSE, WSMsgType.CLOSED):
            value = {"closed": True, "code": ws.close_code or message.data}
        else:
            raise AssertionError(
                f"Unexpected WebSocket frame {message.type}: {message.data}"
            )
        event(
            "log",
            name,
            "Server → client",
            ws_client=name,
            ws_direction="receive",
            ws_body=value,
        )
        return value

    async def http(self, method, path, data=None, status=200, headers=None):
        event(
            "log",
            "client",
            f"{method} {path}",
            http_method=method,
            http_url=self.url + path,
            request_body=data,
        )
        async with self.session.request(
            method, self.url + path, json=data, headers=headers
        ) as response:
            body = await response.text()
            event(
                "log",
                "response",
                f"{response.status}: {body[:1200]}",
                http_method=method,
                http_url=self.url + path,
                http_status=response.status,
                response_body=body,
            )
            assert response.status == status, (response.status, body)
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return body

    async def graphql(self, query, variables=None):
        result = await self.http(
            "POST", "/graphql", {"query": query, "variables": variables or {}}
        )
        assert "errors" not in result, result
        return result["data"]


def token(module, subject="1", expired=False):
    return jwt.encode(
        {
            "sub": subject,
            "exp": datetime.now(timezone.utc)
            + timedelta(seconds=-10 if expired else 60),
        },
        module.DEMO_SECRET,
        algorithm="HS256",
    )


async def game_round(wire, moves, invalid=False, disconnect=False):
    x = await wire.connect("X")
    welcome = await wire.receive(x, "X")
    assert welcome["symbol"] == "X"
    assert (await wire.receive(x, "X"))["status"] == "waiting"
    o = await wire.connect("O")
    assert (await wire.receive(o, "O"))["symbol"] == "O"
    assert (await wire.receive(x, "X"))["status"] == "playing"
    assert (await wire.receive(o, "O"))["status"] == "playing"
    if invalid:
        await wire.send(o, {"cell": 0}, "O")
        assert (await wire.receive(o, "O"))["type"] == "error"
        await wire.send(x, {"cell": True}, "X")
        assert (await wire.receive(x, "X"))["type"] == "error"
    state = None
    for index, cell in enumerate(moves):
        actor, symbol = (x, "X") if index % 2 == 0 else (o, "O")
        await wire.send(actor, {"cell": cell}, symbol)
        state = await wire.receive(x, "X")
        assert await wire.receive(o, "O") == state
    if disconnect:
        await o.close()
        state = await wire.receive(x, "X")
        assert state["status"] == "disconnected"
    await x.close()
    await o.close()
    return state


async def demonstrate(number, module, app, wire):
    if number in (1, 8):
        ws = await wire.connect()
        await wire.send(ws, "Hello")
        assert await wire.receive(ws) == "Server: Hello"
        if number == 8:
            await asyncio.sleep(0.08)
        await ws.close()
    elif number == 2:
        from client import send_messages

        replies = await send_messages(
            wire.url.replace("http://", "ws://") + "/ws"
        )
        assert replies == [
            "Server: Hello",
            "Server: How are you?",
            "Server: Goodbye",
        ]
        for reply in replies:
            event(
                "log",
                "client",
                reply,
                ws_client="client",
                ws_direction="receive",
                ws_body=reply,
            )
        metric("Echo replies", len(replies))
    elif number == 3:
        first = await wire.connect("A")
        assert await wire.receive(first, "A") == "You are client number 1"
        second = await wire.connect("B")
        assert await wire.receive(second, "B") == "You are client number 2"
        await first.close()
        await second.close()
    elif number in (4, 5, 6):
        result = await wire.graphql(
            "query ($id: ID!) { user(id: $id) { id name email } }", {"id": "1"}
        )
        assert result["user"]["name"] == "Anna"
        absent = await wire.graphql('{ user(id: "99") { name } }')
        assert absent["user"] is None
        if number >= 5:
            assert len((await wire.graphql("{ users { name } }"))["users"]) == 2
        if number == 6:
            created = await wire.graphql(
                'mutation { createUser(name:"Alex", email:"alex@example.com") { id name } }'
            )
            assert created["createUser"] == {"id": "3", "name": "Alex"}
            assert len((await wire.graphql("{ users { name } }"))["users"]) == 3
    elif number in (7, 9):
        a = await wire.connect("Anna")
        b = await wire.connect("Jan")
        if number == 9:
            await wire.send(a, "Anna", "Anna")
            await wire.send(b, "Jan", "Jan")
        await wire.receive(a, "Anna")
        await wire.receive(b, "Jan")
        await wire.send(a, "Hello room", "Anna")
        expected = "Anna: Hello room" if number == 9 else "Hello room"
        assert await wire.receive(a, "Anna") == expected
        assert await wire.receive(b, "Jan") == expected
        metric("Broadcast recipients", 2)
        await a.close()
        await b.close()
    elif number in (10, 12):
        result = await wire.graphql(
            "{ users { name posts { title author { name } } } }"
        )
        assert result["users"][0]["posts"][0]["author"]["name"] == "Anna"
        if number == 12:
            filtered = await wire.graphql(
                '{ posts(authorId:"2") { title } searchUsers(name:"AN") { name } }'
            )
            assert filtered["posts"] == [{"title": "Async"}]
            assert filtered["searchUsers"] == [
                {"name": "Anna"},
                {"name": "Jan"},
            ]
    elif number == 11:
        metric("Production ping interval", 30, "s")
        metric("Production pong timeout", 60, "s")
        event(
            "log",
            "demo",
            "Accelerated demonstration: interval 0.05 s, timeout 0.15 s",
        )
        alive = await wire.connect("responding")
        for _ in range(3):
            assert await wire.receive(alive, "responding") == "ping"
            await wire.send(alive, "pong", "responding")
        await alive.close()
        silent = await wire.connect("silent")
        while True:
            result = await wire.receive(silent, "silent")
            if isinstance(result, dict) and result.get("closed"):
                assert result["code"] == 1001
                break
        metric("Silent client disconnected", True)
        await silent.close()
    elif number == 13:
        a = await wire.connect("room-one")
        b = await wire.connect("room-two")
        await wire.receive(a, "room-one")
        await wire.receive(b, "room-two")
        await wire.send(a, "/join one", "room-one")
        await wire.receive(a, "room-one")
        await wire.send(b, "/join two", "room-two")
        await wire.receive(b, "room-two")
        await wire.send(a, "Private room message", "room-one")
        assert await wire.receive(a, "room-one") == "Private room message"
        try:
            await asyncio.wait_for(b.receive(), 0.12)
            raise AssertionError("Message leaked to another room")
        except asyncio.TimeoutError:
            metric("Room isolation verified", True)
        await wire.send(b, "/join one", "room-two")
        await wire.receive(b, "room-two")
        await wire.send(a, "Together", "room-one")
        assert await wire.receive(a, "room-one") == "Together"
        assert await wire.receive(b, "room-two") == "Together"
        await a.close()
        await b.close()
    elif number == 14:
        for label, credential, accepted in [
            ("valid", token(module), True),
            ("invalid", "broken", False),
            ("expired", token(module, expired=True), False),
        ]:
            ws = await wire.connect(label)
            await wire.send(ws, credential, label, redact=True)
            result = await wire.receive(ws, label)
            if accepted:
                assert result["user_id"] == "1"
                await wire.send(ws, "Authenticated hello", label)
                assert (
                    await wire.receive(ws, label)
                    == "Server: Authenticated hello"
                )
            else:
                assert result["closed"] and result["code"] == 1008
            await ws.close()
    elif number == 15:
        ws = await wire.connect(
            "subscriber", protocols=("graphql-transport-ws",)
        )
        await wire.send(ws, {"type": "connection_init"}, "subscriber")
        assert (await wire.receive(ws, "subscriber"))[
            "type"
        ] == "connection_ack"
        await wire.send(
            ws,
            {
                "id": "new-user",
                "type": "subscribe",
                "payload": {
                    "query": "subscription { userRegistered { id name } }"
                },
            },
            "subscriber",
        )
        await asyncio.wait_for(module.subscription_ready.wait(), 3)
        await wire.graphql(
            'mutation { createUser(name:"Alex", email:"alex@example.com") { id } }'
        )
        event_data = await wire.receive(ws, "subscriber")
        assert (
            event_data["type"] == "next"
            and event_data["payload"]["data"]["userRegistered"]["name"]
            == "Alex"
        )
        await wire.send(
            ws, {"id": "new-user", "type": "complete"}, "subscriber"
        )
        await ws.close()
        metric("Real subscription event", True)
    elif number == 16:
        first = await wire.connect("Anna")
        await wire.send(first, "Anna", "Anna")
        assert (await wire.receive(first, "Anna"))["messages"] == []
        await wire.send(first, "Saved in SQLite", "Anna")
        assert (await wire.receive(first, "Anna"))["body"] == "Saved in SQLite"
        second = await wire.connect("Jan")
        await wire.send(second, "Jan", "Jan")
        history = await wire.receive(second, "Jan")
        assert (
            len(history["messages"]) == 1
            and history["messages"][0]["body"] == "Saved in SQLite"
        )
        await first.close()
        await second.close()
        metric("History persisted", True)
    elif number == 17:
        await wire.http("POST", "/reset")
        naive = await wire.graphql("{ users { name naivePosts } }")
        before = (await wire.http("GET", "/stats"))["fetch_count"]
        await wire.http("POST", "/reset")
        batched = await wire.graphql("{ users { name posts } }")
        after = (await wire.http("GET", "/stats"))["fetch_count"]
        assert [u["naivePosts"] for u in naive["users"]] == [
            u["posts"] for u in batched["users"]
        ]
        assert before == 3 and after == 1, (before, after)
        metric("Naive fetches", before)
        metric("DataLoader fetches", after)
    elif number == 18:
        a = await wire.connect("user-1")
        b = await wire.connect("user-2")
        await wire.send(a, token(module, "1"), "user-1", True)
        await wire.receive(a, "user-1")
        await wire.send(b, token(module, "2"), "user-2", True)
        await wire.receive(b, "user-2")
        await wire.http(
            "POST",
            "/notifications",
            {"user_id": "1", "text": "New message"},
            status=401,
        )
        await wire.http(
            "POST",
            "/notifications",
            {"user_id": "1", "text": "New message"},
            status=201,
            headers={"Authorization": "Bearer " + token(module, "admin")},
        )
        assert (await wire.receive(a, "user-1"))["text"] == "New message"
        try:
            await asyncio.wait_for(b.receive(), 0.12)
            raise AssertionError("Notification leaked to another user")
        except asyncio.TimeoutError:
            metric("Recipient isolation verified", True)
        await a.close()
        await b.close()
    elif number == 19:
        ws = await wire.connect()
        await wire.receive(ws)
        await wire.send(ws, "Live and saved")
        assert await wire.receive(ws) == "Live and saved"
        result = await wire.graphql(
            "{ history { nickname body } profiles { id name } }"
        )
        assert result["history"] == [
            {"nickname": "Guest", "body": "Live and saved"}
        ]
        assert len(result["profiles"]) == 2
        await ws.close()
    elif number == 20:
        state = await game_round(wire, [0, 3, 1, 4, 2], invalid=True)
        assert state["status"] == "winner:X"
        metric("Winner", state["status"])
    else:
        raise ValueError("Unknown task")


async def run(number, module):
    app = (
        module.create_app(interval=0.05, timeout=0.15)
        if number == 11
        else module.create_app()
    )
    async with server(app) as url:
        async with ClientSession(timeout=ClientTimeout(total=10)) as session:
            with span("demonstration", "Network exchange"):
                await demonstrate(number, module, app, Wire(session, url))
    if hasattr(module, "clients"):
        clients = module.clients
        assert (
            not any(clients.values())
            if isinstance(clients, dict)
            else not clients
        )
    if hasattr(module, "rooms"):
        assert not module.rooms
    if hasattr(module, "subscribers"):
        assert not module.subscribers
    metric("Scenario verified", True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, choices=range(1, 21))
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8134)
    args = parser.parse_args()
    runtime = ROOT / ".runtime"
    runtime.mkdir(exist_ok=True)
    os.environ["LESSON34_WORKDIR"] = tempfile.mkdtemp(
        prefix=f"task{args.number:02}-", dir=runtime
    )
    sys.path.insert(0, str(ROOT / "examples" / f"task{args.number:02}"))
    module = importlib.import_module("main")
    if args.serve:
        app = module.create_app()

        async def ready(request):
            return web.json_response({"lesson": 34, "task": args.number})

        app.router.add_get("/__ready", ready)
        web.run_app(app, host="127.0.0.1", port=args.port)
    else:
        launch(lambda options: asyncio.run(run(args.number, module)))


if __name__ == "__main__":
    main()
