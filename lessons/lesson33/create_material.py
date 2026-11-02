"""Compile actual task sources, authored forecasts and matching teaching ranges."""

import ast
import json
from pathlib import Path

from course_content import PIPELINES, TOPICS, bi
from teaching import CALLS, FUNCTIONS, detailed_steps, pair

ROOT = Path(__file__).resolve().parent
INTRO_KEYS = {
    1: ["FastAPI"],
    2: ["Path"],
    3: ["Query", "HTTPException"],
    4: ["Field", "model_dump"],
    5: ["values"],
    6: ["Response", "HTTPException"],
    7: ["EmailStr"],
    8: ["FastAPI"],
    9: ["APIRouter", "include_router"],
    10: ["Depends", "Header"],
    11: ["Field"],
    12: ["Field", "isalnum"],
    13: ["Depends", "flush"],
    14: ["ForeignKey", "selectinload"],
    15: ["add_task"],
    16: ["call_next", "to_thread"],
    17: ["database_lifespan"],
    18: ["where", "offset"],
    19: ["Depends", "selectinload"],
    20: ["body", "add_task"],
}


def quick_steps(sources, number):
    result = []

    def add(file, node, name, body):
        result.append(
            dict(
                file=file,
                start=node.lineno,
                end=node.end_lineno,
                name=name,
                body=body,
                details=[],
            )
        )

    for file, source in sources.items():
        tree = ast.parse(source)
        if number in (19, 20):
            # Project slides follow modules and coherent features instead of one per method.
            notes = {
                "main.py": (
                    "Uruchomienie i middleware / Startup and middleware",
                    "Aplikacja dołącza routery i zarządza PostgreSQL przez lifespan. Konflikty bazy stają się 409. W zadaniu 20 middleware sprawdza body przed endpointem.",
                    "The app includes routers and manages PostgreSQL via lifespan. Database conflicts become 409. In task 20 middleware checks the body before endpoints.",
                ),
                "models.py": (
                    "Tabele i relacje / Tables and relationships",
                    "User → Post → Comment są powiązane kluczami obcymi. Post.comments udostępnia kolekcję; kasowanie w bazie usuwa zależne rekordy.",
                    "Foreign keys connect User → Post → Comment. Post.comments exposes the collection; database deletes remove dependent rows.",
                ),
                "schemas.py": (
                    "Kontrakt danych / Data contract",
                    "Modele Pydantic ograniczają długości tekstów. JSON posta nie zawiera user_id: autor zostanie ustalony po kluczu.",
                    "Pydantic models constrain text lengths. Post JSON contains no user_id: the key determines its author.",
                ),
                "auth.py": (
                    "Rozpoznanie autora / Resolve the author",
                    "Demonstracyjny klucz wskazuje ID konta. Osobna sesja potwierdza istnienie użytkownika. Brak klucza lub użytkownika daje 401. Zmiana nazwy konta nie zmienia jego ID.",
                    "A demo key maps to an account ID. A separate session checks the user exists. Missing keys or users give 401. Renaming an account does not change its ID.",
                ),
                "routers/users.py": (
                    "CRUD użytkowników / User CRUD",
                    "Router obsługuje tworzenie, listę, odczyt, zmianę i usuwanie. Zmiana i usunięcie wymagają właściciela konta.",
                    "The router implements create, list, read, update and delete. Changes and deletion require account ownership.",
                ),
            }
            if file in notes:
                title, pl, en = notes[file]
                nodes = tree.body
                stub = ast.Pass(
                    lineno=nodes[0].lineno, end_lineno=nodes[-1].end_lineno
                )
                add(file, stub, title, pair(pl, en))
                continue
            if file == "routers/posts.py":
                groups = [
                    (
                        "Tworzenie i odczyt / Create and read",
                        ("create_post", "list_posts", "get_post"),
                        "Autor pochodzi z dependency. Zapis jest w transakcji; odczyty zwracają słowniki JSON.",
                        "The dependency supplies authorship. Writes use a transaction; reads return JSON dictionaries.",
                    ),
                    (
                        "Edycja i usuwanie / Edit and delete",
                        ("replace_post", "delete_post"),
                        "Przed zmianą porównujemy post.user_id z actor. Cudzy użytkownik dostanie 403; właściciel może zmienić lub usunąć post.",
                        "Compare post.user_id with actor before changing anything. Other users get 403; the owner can edit or delete.",
                    ),
                    (
                        "Komentarze i eager loading / Comments and eager loading",
                        ("add_comment", "post_with_comments"),
                        "Komentarz zapisujemy przed zaplanowaniem powiadomienia. selectinload pobiera kolekcję do zagnieżdżonego JSON bez leniwego I/O.",
                        "Save the comment before scheduling notification. selectinload fetches the collection for nested JSON without lazy I/O.",
                    ),
                    (
                        "Praca w tle / Background work",
                        ("notify_author", "analyze_sentiment"),
                        "Powiadomienie trafia do pliku po odpowiedzi HTTP. W zadaniu 20 reguła great/bad zapisuje również symulowany sentyment.",
                        "Notification is written to a file after the HTTP response. In task 20 a great/bad rule also records simulated sentiment.",
                    ),
                    (
                        "Podsumowanie / Summary",
                        ("summarize",),
                        "Pierwszych 12 słów tworzy lokalną symulację. Pole mode jasno informuje, że nie używamy modelu językowego.",
                        "The first 12 words form a local simulation. mode clearly states that no language model is used.",
                    ),
                ]
                for title, names, pl, en in groups:
                    nodes = [
                        node
                        for node in tree.body
                        if isinstance(
                            node, (ast.FunctionDef, ast.AsyncFunctionDef)
                        )
                        and node.name in names
                    ]
                    if nodes:
                        stub = ast.Pass(
                            lineno=min(n.lineno for n in nodes),
                            end_lineno=max(n.end_lineno for n in nodes),
                        )
                        add(file, stub, title, pair(pl, en))
                continue
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        if classes:
            stub = ast.Pass(
                lineno=classes[0].lineno, end_lineno=classes[-1].end_lineno
            )
            add(
                file,
                stub,
                "Modele i pola / Models and fields",
                pair(
                    "Modele Pydantic opisują wejście i odpowiedź; modele ORM opisują tabele. Field sprawdza ograniczenia. ForeignKey i relationship łączą rekordy, gdy występują w zadaniu.",
                    "Pydantic models describe input/output; ORM models describe tables. Field checks constraints. ForeignKey and relationship link records when present.",
                ),
            )
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                pl, en = FUNCTIONS[node.name]
                # At most one key mechanism supplements the brief functional overview.
                calls = [n for n in ast.walk(node) if isinstance(n, ast.Call)]
                for key in (
                    "selectinload",
                    "flush",
                    "add_task",
                    "to_thread",
                    "call_next",
                ):
                    if any(
                        ast.unparse(call.func).rsplit(".", 1)[-1] == key
                        for call in calls
                    ):
                        extra = CALLS[key]
                        pl += " " + extra[0]
                        en += " " + extra[1]
                        break
                add(file, node, node.name, pair(pl, en))
            elif isinstance(node, ast.Assign) and any(
                isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name)
                and n.func.id == "FastAPI"
                for n in ast.walk(node)
            ):
                add(
                    file,
                    node,
                    "Aplikacja / Application",
                    pair(
                        "Tworzymy aplikację. Modele i dekoratory poniżej/obok określają jej kontrakt; serwer uruchomi ją osobno.",
                        "Create the application. Models and decorators define its contract; a server starts it separately.",
                    ),
                )
    if not 1 <= len(result) <= 20:
        raise ValueError(f"Quick slide count for task {number}: {len(result)}")
    return result


def build():
    records = []
    for number, topic in enumerate(TOPICS, 1):
        title, intro, forecast, outcome, question, answer = map(bi, topic)
        folder = ROOT / "examples" / f"task{number:02}"
        paths = sorted(
            (p for p in folder.rglob("*.py") if p.name != "__init__.py"),
            key=lambda p: (p.name != "main.py", str(p)),
        )
        sources = {
            path.relative_to(folder).as_posix(): path.read_text(
                encoding="utf-8"
            )
            for path in paths
        }
        steps = [
            step
            for file, source in sources.items()
            for step in detailed_steps(file, source)
        ]
        quick = quick_steps(sources, number)
        record = dict(
            number=number,
            title=title,
            intro=intro,
            forecast=forecast,
            pipeline=bi(PIPELINES[number - 1]),
            takeaway=outcome,
            watch=pair(
                "Najpierw przewidź odpowiedzi. Pokaz wyśle prawdziwe żądania HTTP, sprawdzi statusy i pokaże dane wejścia/wyjścia.",
                "Predict responses first. The demo sends real HTTP requests, verifies statuses and displays input/output.",
            ),
            question=question,
            answer=answer,
            extra_question=pair(
                "Zmień jedno pole wejścia. Który etap jako pierwszy zareaguje: walidacja, dependency, endpoint czy baza?",
                "Change one input field. Which stage reacts first: validation, dependency, endpoint or database?",
            ),
            extra_answer=pair(
                "Prześledź kolejno model i ograniczenia, dependency, warunki w funkcji oraz ograniczenia tabel. Przewidź status i porównaj go z odpowiedzią.",
                "Trace the model constraints, dependency, function conditions and table constraints. Predict the status and compare it with the response.",
            ),
            caveat=pair(
                "Pokaz działa lokalnie, w osobnym procesie i z własnymi danymi. PostgreSQL jest prawdziwy; mail i AI są symulowane. Klucze demonstracyjne nie stanowią pełnego systemu logowania. BackgroundTasks nie gwarantuje trwałej kolejki.",
                "The demo runs locally in a separate process with its own data. PostgreSQL is real; email and AI are simulated. Demo keys are not a complete authentication system. BackgroundTasks is not a durable queue.",
            ),
            adaptation=pair(
                "Kod jest po angielsku. Zadania 9, 19 i 20 mają kilka plików. Używamy Pydantic v2, lifespan i osobnej bazy lesson33. W bazie ceny są w groszach. Każdy pokaz odtwarza własny schemat; pliki wynikowe pozostają w .runtime.",
                "Code uses English. Tasks 9, 19 and 20 contain several files. We use Pydantic v2, lifespan and a separate lesson33 database. Database prices use cents. Each demo creates its own schema; evidence files remain in .runtime.",
            ),
            presets=[dict(label="Pełny pokaz / Full demonstration", value={})],
            terms=[
                dict(name=key, body=pair(*CALLS[key]))
                for key in INTRO_KEYS[number]
            ],
            steps=dict(
                file="main.py",
                source=sources["main.py"],
                sources={
                    file: dict(source=value) for file, value in sources.items()
                },
                steps=steps,
            ),
        )
        if len(steps) > 20:
            record["steps"]["quick"] = quick
        records.append(record)
        docs = ROOT / "explanations"
        docs.mkdir(exist_ok=True)
        lines = [
            f"# Zadanie {number:02} — {title['pl']}",
            "",
            "## Zanim przeczytasz kod",
            "",
            forecast["pl"],
            "",
            outcome["pl"],
            "",
            "## Dokładne wyjaśnienie",
            "",
        ]
        for step in steps:
            fragment = "\n".join(
                sources[step["file"]].splitlines()[
                    step["start"] - 1 : step["end"]
                ]
            )
            lines.extend([
                f"### {step['file']}: {step['start']}–{step['end']}",
                "",
                "```python",
                fragment,
                "```",
                "",
                step["body"]["pl"],
                "",
            ])
        (docs / f"task{number:02}.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )
    (ROOT / "material.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for record in records:
        print(
            f"Task {record['number']:02}: {len(record['steps']['steps'])} detailed; {len(record['steps'].get('quick', []))} quick"
        )


if __name__ == "__main__":
    build()
