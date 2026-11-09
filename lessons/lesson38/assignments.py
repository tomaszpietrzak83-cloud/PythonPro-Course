"""Paginated assignments from the original tasks.md without rewriting them."""

import math
import re
from pathlib import Path

from course_content import ENGLISH


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
