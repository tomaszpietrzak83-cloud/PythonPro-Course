"""Source-bound notes: statement ranges come from the current Python AST."""
import ast
import html
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from course_content import pair, ROWS

FUNCTION_TASKS = dict(zip([
    'check_service_health', 'backup_directory', 'list_regions', 'create_s3_bucket',
    'upload_jpg', 'list_instances', 'parse_logs', 'read_environment', 'auto_stop',
    'backup_with_rotation', 'sync_buckets', 'report', 'deployment_pipeline',
    'deploy_website', 'monitor_once', 'simulate_scaling', 'process_images',
    'compare', 'restore_from_backup', 'optimize_costs'], range(20)))


def describe(node):
    code = ast.unparse(node)
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        if node.name in FUNCTION_TASKS:
            row = ROWS[FUNCTION_TASKS[node.name]]
            return pair(row[2]+' '+row[4], row[3]+' '+row[5])
        doc = ast.get_docstring(node)
        return pair(doc or f'Funkcja {node.name}: argumenty są wejściem; prześledź warunki i return poniżej.',
                    doc or f'Function {node.name}: arguments are inputs; follow the conditions and returns below.')
    descriptions = {
        ast.Import: ('Importuje bibliotekę używaną w dalszym kodzie.', 'Imports a library used below.'),
        ast.ImportFrom: ('Udostępnia wskazane nazwy z biblioteki.', 'Imports the named library objects.'),
        ast.If: ('Sprawdza warunek; tylko spełniona gałąź zmieni wynik.', 'Tests the condition; only the matching branch changes the result.'),
        ast.For: ('Przetwarza po kolei elementy kolekcji. Zwróć uwagę na filtry i continue.', 'Processes collection items in order. Look at filters and continue.'),
        ast.While: ('Powtarza blok, dopóki warunek jest prawdziwy.', 'Repeats the body while the condition holds.'),
        ast.With: ('Otwiera zasób i zapewnia jego zamknięcie po wyjściu z bloku.', 'Opens a resource and closes it on leaving the block.'),
        ast.Try: ('Wykonuje operację mogącą zgłosić wyjątek; except obsługuje wskazane błędy.', 'Runs an operation that may raise; except handles specified failures.'),
        ast.Return: ('Kończy to wywołanie funkcji i przekazuje wynik do wywołującego.', 'Ends this function call and passes its result to the caller.'),
        ast.Assign: ('Oblicza prawą stronę i przypisuje wynik do nazw po lewej.', 'Evaluates the right side and assigns the result to the targets.'),
        ast.Assert: ('Sprawdza warunek poprawności pokazu; fałsz zgłasza AssertionError.', 'Checks a demonstration invariant; false raises AssertionError.'),
        ast.ClassDef: ('Grupuje dane i metody opisane w bloku klasy.', 'Groups the data and methods defined in the class.'),
    }
    pl, en = descriptions.get(type(node), ('Wykonuje instrukcję podaną poniżej. Sprawdź jej argumenty i otaczający warunek.', 'Executes the statement below. Inspect its arguments and enclosing condition.'))
    return pair(pl+'\n\n'+code, en+'\n\n'+code)


def build(source, file):
    if file.endswith('.json'):
        notes, rows = {}, []
        for line, text in enumerate(source.splitlines(), 1):
            key = f'{file}:line:{line}'
            notes[key] = dict(id=key, file=file, kind='line', start=line, end=line,
                              title=f'{file} · L{line}', body=pair('Konfiguracja JSON odczytywana przez ConfigManager.', 'JSON configuration read by ConfigManager.'), expression=text)
            rows.append(dict(line=line, html=html.escape(text), line_note=key, block_note=key))
        return dict(source=source, notes=notes, annotated_rows=rows)
    tree = ast.parse(source)
    statements = [n for n in ast.walk(tree) if isinstance(n, ast.stmt)]
    blocks = [n for n in statements if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.If, ast.For, ast.While, ast.With, ast.Try))]
    notes, rows = {}, []
    def note(node, line, kind):
        start = node.lineno if node else line
        end = node.end_lineno if node else line
        key = f'{file}:{kind}:{start}:{end}'
        notes[key] = dict(id=key, file=file, kind=kind, start=start, end=end,
                          title=f'{file} · L{start}–{end}', body=describe(node) if node else pair('Odstęp lub komentarz; bez wykonywanej instrukcji.', 'Whitespace or comment; no executed statement.'), expression=None)
        return key
    for line, text in enumerate(source.splitlines(), 1):
        matches = [n for n in statements if n.lineno <= line <= n.end_lineno]
        node = min(matches, key=lambda n: n.end_lineno-n.lineno) if matches else None
        enclosing = [n for n in blocks if n.lineno <= line <= n.end_lineno]
        block = min(enclosing, key=lambda n: n.end_lineno-n.lineno) if enclosing else node
        line_note, block_note = note(node, line, 'line'), note(block, line, 'block')
        rendered = highlight(text, PythonLexer(), HtmlFormatter(nowrap=True)).rstrip('\n')
        # Whole function/call statement is keyboard reachable and can be pinned.
        if text.strip():
            rendered = f'<span class="code-symbol" data-note="{html.escape(line_note)}" tabindex="0" role="button" aria-label="L{line}">{rendered}</span>'
        rows.append(dict(line=line, html=rendered, line_note=line_note, block_note=block_note))
    return dict(source=source, notes=notes, annotated_rows=rows)
