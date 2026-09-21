import ast
import builtins
import io
import keyword
import token
import tokenize
from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.utils.html import escape

TASKS = [
    ("01", "Zadanie 1 - Instalacja i projekt", "01.py"),
    ("02", "Zadanie 2 - Uruchomienie serwera", "02.py"),
    ("03", "Zadanie 3 - Tworzenie aplikacji", "03.py"),
    ("04", "Zadanie 4 - Konfiguracja bazy danych", "04.py"),
    ("05", "Zadanie 5 - Superuzytkownik", "05.py"),
    ("06", "Zadanie 6 - Definicja modelu", "06.py"),
    ("07", "Zadanie 7 - Migracje", "07.py"),
    ("08", "Zadanie 8 - Rejestracja w panelu admina", "08.py"),
    ("09", "Zadanie 9 - Zarzadzanie danymi", "09.py"),
    ("10", "Zadanie 10 - Personalizacja panelu admina", "10.py"),
]

BUILTIN_NAMES = set(dir(builtins))
CONSTANT_NAMES = {"True", "False", "None"}


def get_code_part(lines, start, end):
    if not lines:
        return ""

    start_line, start_column = start
    end_line, end_column = end
    if start_line > len(lines):
        return ""
    if end_line > len(lines):
        end_line = len(lines)
        end_column = len(lines[-1])

    if start_line == end_line:
        return lines[start_line - 1][start_column:end_column]

    parts = [lines[start_line - 1][start_column:]]
    parts.extend(lines[start_line : end_line - 1])
    parts.append(lines[end_line - 1][:end_column])
    return "".join(parts)


def token_class(token_type, token_text):
    if token_type == token.COMMENT:
        return "comment"
    if token_type == token.STRING:
        return "string"
    if token_type == token.NUMBER:
        return "number"
    if token_type == token.OP:
        return "operator"
    if token_type == token.NAME:
        if token_text in keyword.kwlist:
            return "keyword"
        if token_text in CONSTANT_NAMES:
            return "constant"
        if token_text in BUILTIN_NAMES:
            return "builtin"
    return ""


def highlight_python_code(source):
    lines = source.splitlines(keepends=True)
    highlighted_parts = []
    previous_end = (1, 0)

    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for current_token in tokens:
            token_type = current_token.type
            token_text = current_token.string
            start = current_token.start
            end = current_token.end

            if token_type in {
                tokenize.ENCODING,
                token.ENDMARKER,
                token.INDENT,
                token.DEDENT,
            }:
                continue

            highlighted_parts.append(
                escape(get_code_part(lines, previous_end, start))
            )

            css_class = token_class(token_type, token_text)
            escaped_text = escape(token_text)
            if css_class:
                highlighted_parts.append(
                    f'<span class="code-{css_class}">{escaped_text}</span>'
                )
            else:
                highlighted_parts.append(escaped_text)

            previous_end = end

        if lines:
            end_position = (len(lines), len(lines[-1]))
            highlighted_parts.append(
                escape(get_code_part(lines, previous_end, end_position))
            )
        return "".join(highlighted_parts)
    except tokenize.TokenError:
        return escape(source)


def is_python_code(source):
    try:
        compile(source.strip(), "<solution>", "exec")
    except SyntaxError:
        return False
    return True


def render_code_block(source):
    source = source.strip("\n")
    if is_python_code(source):
        code = highlight_python_code(source)
    else:
        code = escape(source)

    return f"<pre><code>{code}</code></pre>"


def render_solution_file(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return render_code_block(source)

    sections = []
    for node in tree.body:
        name = None
        value = None

        if isinstance(node, ast.Assign) and isinstance(
            node.value, ast.Constant
        ):
            value = node.value.value
            if node.targets and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
        elif isinstance(node, ast.AnnAssign) and isinstance(
            node.value, ast.Constant
        ):
            value = node.value.value
            if isinstance(node.target, ast.Name):
                name = node.target.id

        if isinstance(value, str) and name:
            sections.append(
                f"""
                <section class="solution-section">
                    <h2>{escape(name)}</h2>
                    {render_code_block(value)}
                </section>
                """
            )

    if not sections:
        return render_code_block(source)

    return "\n".join(sections)


def index(request):
    task_links = "\n".join(
        f"""
        <li>
            <a href="{reverse("task_detail", args=[number])}">
                <span>/zadania/{number}/</span>
                {escape(title)}
            </a>
        </li>
        """
        for number, title, _ in TASKS
    )

    html = f"""
    <!doctype html>
    <html lang="pl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Lekcja 19 - zadania</title>
        <style>
            body {{
                margin: 0;
                min-height: 100vh;
                background: #f4f7fb;
                color: #172033;
                font-family: Arial, sans-serif;
            }}

            main {{
                width: min(920px, calc(100% - 32px));
                margin: 0 auto;
                padding: 48px 0;
            }}

            h1 {{
                margin: 0 0 8px;
                font-size: 2rem;
            }}

            p {{
                margin: 0 0 28px;
                color: #5c667a;
                font-size: 1rem;
                line-height: 1.6;
            }}

            ul {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 12px;
                padding: 0;
                margin: 0;
                list-style: none;
            }}

            a {{
                display: block;
                min-height: 72px;
                padding: 16px;
                border: 1px solid #d8deea;
                border-radius: 8px;
                background: #ffffff;
                color: #172033;
                text-decoration: none;
                box-shadow: 0 10px 24px rgba(33, 48, 76, 0.07);
            }}

            a:hover {{
                border-color: #2f6fed;
                box-shadow: 0 12px 28px rgba(47, 111, 237, 0.14);
            }}

            span {{
                display: block;
                margin-bottom: 8px;
                color: #2f6fed;
                font-family: Consolas, monospace;
                font-size: 0.95rem;
                font-weight: 700;
            }}
        </style>
    </head>
    <body>
        <main>
            <h1>Lekcja 19 - rozwiazania</h1>
            <p>Linki prowadza do endpointow, ktore prezentuja rozwiazania zadan od 01.py do 10.py.</p>
            <ul>
                {task_links}
            </ul>
        </main>
    </body>
    </html>
    """
    return HttpResponse(html)


def task_detail(request, task_number):
    task = next((task for task in TASKS if task[0] == task_number), None)
    if task is None:
        raise Http404("Nie ma takiego zadania.")

    _, title, filename = task
    file_path = Path(settings.PROJECT_ROOT) / filename
    if not file_path.exists():
        raise Http404("Plik z rozwiazaniem nie istnieje.")

    solution_html = render_solution_file(file_path.read_text(encoding="utf-8"))
    back_url = reverse("index")
    html = f"""
    <!doctype html>
    <html lang="pl">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{escape(title)}</title>
        <style>
            body {{
                margin: 0;
                min-height: 100vh;
                background: #f4f7fb;
                color: #172033;
                font-family: Arial, sans-serif;
            }}

            main {{
                width: min(980px, calc(100% - 32px));
                margin: 0 auto;
                padding: 40px 0;
            }}

            a {{
                color: #2f6fed;
                font-weight: 700;
                text-decoration: none;
            }}

            h1 {{
                margin: 20px 0 8px;
                font-size: 1.8rem;
            }}

            p {{
                margin: 0 0 18px;
                color: #5c667a;
            }}

            .solution-section {{
                margin-top: 20px;
            }}

            .solution-section h2 {{
                margin: 0 0 8px;
                color: #334155;
                font-size: 1rem;
                font-family: Consolas, monospace;
            }}

            pre {{
                overflow-x: auto;
                padding: 18px;
                border: 1px solid #293142;
                border-radius: 8px;
                background: #1e1e1e;
                color: #d4d4d4;
                box-shadow: 0 10px 24px rgba(33, 48, 76, 0.07);
                line-height: 1.5;
                tab-size: 4;
            }}

            code {{
                font-family: Consolas, monospace;
                font-size: 0.95rem;
            }}

            .code-keyword {{
                color: #569cd6;
            }}

            .code-string {{
                color: #ce9178;
            }}

            .code-comment {{
                color: #6a9955;
            }}

            .code-number {{
                color: #b5cea8;
            }}

            .code-builtin {{
                color: #dcdcaa;
            }}

            .code-constant {{
                color: #4fc1ff;
            }}

            .code-operator {{
                color: #d4d4d4;
            }}
        </style>
    </head>
    <body>
        <main>
            <a href="{back_url}">Powrot do listy zadan</a>
            <h1>{escape(title)}</h1>
            <p>Endpoint: /zadania/{escape(task_number)}/ | Plik z rozwiazaniem: {escape(filename)}</p>
            {solution_html}
        </main>
    </body>
    </html>
    """
    return HttpResponse(html)
