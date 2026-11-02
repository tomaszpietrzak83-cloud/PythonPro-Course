"""Paginated assignments from the original tasks.md without rewriting them."""

import math
import re
from pathlib import Path

ENGLISH = [
    "Create a WebSocket echo server. Reply to every incoming text with the prefix Server:.",
    "Write a WebSocket client sending Hello, How are you? and Goodbye. Receive and print the server reply after each message.",
    "Greet each new client with its current active connection count. X is the number of active connections.",
    "Create a GraphQL User type with id, name and email. Add user(id: ID!): User, reading from a fake list.",
    "Extend task 4 with users: [User], returning all users.",
    "Add createUser(name: String!, email: String!): User mutation. Create a user, append it to a fake list and return it.",
    "Broadcast every incoming WebSocket message to every connected client. Store active sockets in a set.",
    "Measure each WebSocket connection duration. Record its start and print elapsed time on disconnection.",
    "Build a chat where the initial client message supplies a nickname. Broadcast subsequent texts as Nick: message.",
    "Create GraphQL User and Post types. User.posts returns the user’s posts; Post.author returns the author. Use fake lists.",
    "Send text ping every 30 seconds. Clients must reply pong. Disconnect a client if no pong arrives within 60 seconds.",
    "Add posts(authorId: ID): [Post] and searchUsers(name: String): [User]. Filter by author ID and by a substring of the user name.",
    "Implement chat rooms. /join room1 joins a room. Broadcast only to clients in the same room.",
    "Authenticate WebSocket via JWT in the initial message. Verify the token, permit chat if valid and close invalid sessions.",
    "Implement a GraphQL registration subscription using strawberry.subscription and AsyncGenerator. Test in GraphiQL or another GraphQL client.",
    "Store chat nickname, body and timestamp in SQLite. Send the latest 50 messages on connection and continue broadcasting new messages.",
    "Use strawberry.dataloader to reduce N+1 when loading users and posts. Measure fetch calls before and after batching.",
    "Build real-time notifications: REST creates notifications; WebSocket delivers them to logged-in users. Select the correct recipient.",
    "Combine GraphQL history and user profiles with real-time WebSocket chat or GraphQL subscriptions.",
    "Build a multiplayer game such as tic-tac-toe over WebSocket. Server owns state, validates moves and broadcasts updates. Handle wins, draws and player disconnections.",
]


def assignment(number, adaptation):
    text = Path(__file__).with_name("tasks.md").read_text(encoding="utf-8")
    sections = re.split(r"^## TASK (\d+) - ", text, flags=re.MULTILINE)
    records = {int(sections[i]): sections[i + 1] for i in range(1, len(sections), 2)}
    title, body = records[number].split("\n", 1)
    return dict(
        source="tasks.md",
        title=title.strip(),
        adaptation=adaptation,
        pages={
            "pl": pages(parse_blocks(body)),
            "en": pages(parse_blocks(ENGLISH[number - 1])),
        },
    )


def parse_blocks(text):
    blocks = []
    lines = text.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("```"):
            language = line[3:]
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append(
                {
                    "kind": "code",
                    "text": "\n".join(code),
                    "language": language,
                }
            )
        elif re.match(r"(?:- |\d+\. )", line):
            items = []
            ordered = not line.startswith("- ")
            while i < len(lines) and re.match(r"\s*(?:- |\d+\. )", lines[i]):
                items.append(re.sub(r"^\s*(?:- |\d+\. )", "", lines[i]))
                i += 1
            blocks.append({"kind": "list", "items": items, "ordered": ordered})
            continue
        elif line.startswith("<p"):
            blocks.append(
                {
                    "kind": "note",
                    "text": re.sub(r"<[^>]+>", "", line),
                }
            )
        else:
            paragraph = [line]
            while (
                i + 1 < len(lines)
                and lines[i + 1].strip()
                and not lines[i + 1].lstrip().startswith(("```", "- ", "<p"))
            ):
                i += 1
                paragraph.append(lines[i].strip())
            blocks.append({"kind": "paragraph", "text": " ".join(paragraph)})
        i += 1
    return blocks


def pages(blocks):
    result, current, weight = [], [], 0
    for block in blocks:
        if block["kind"] == "code":
            size = len(block["text"].splitlines()) + 1
        elif block["kind"] == "list":
            size = sum(max(1, math.ceil(len(item) / 90)) for item in block["items"]) + 1
        else:
            size = max(1, math.ceil(len(block["text"]) / 90)) + 1
        if current and weight + size > 14:
            result.append(current)
            current, weight = [], 0
        current.append(block)
        weight += size
    if current:
        result.append(current)
    return result
