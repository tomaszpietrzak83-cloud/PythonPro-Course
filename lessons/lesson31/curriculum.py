"""Serve reviewed explanations and exact AST ranges from one source snapshot."""
import ast
import json
from pathlib import Path

from assignments import assignment
from method_notes import METHODS, INFRASTRUCTURE

ROOT = Path(__file__).resolve().parent


def bilingual(value):
    pl, en = value.split('|', 1)
    return {'pl': pl, 'en': en}


def pair(value):
    return dict(zip(('pl', 'en'), value))


EXPERIMENTS = [
    ('Co się stanie, jeśli nie przekażesz korutyny do run?', 'What if you never pass the coroutine to run?', 'Jej ciało nie wykona się; korutyna pozostawiona bez await może wygenerować ostrzeżenie.', 'Its body will not run; an unawaited coroutine may produce a warning.'),
    ('Co zmieni range(n) zamiast range(1,n+1)?', 'What changes with range(n) instead of range(1,n+1)?', 'Dla 3 wypisze 0,1,2 zamiast 1,2,3.', 'For 3 it yields 0,1,2 instead of 1,2,3.'),
    ('Co zmieni wcześniejsze utworzenie dwóch Task?', 'What if both Tasks are created before awaiting?', 'Mogą współbieżnie czekać; czas zbliży się do 2 s.', 'Their waits can overlap; duration approaches 2 s.'),
    ('Czy time.sleep zastąpi asyncio.sleep bez skutków?', 'Can time.sleep replace asyncio.sleep without consequences?', 'Nie. Zablokuje wątek pętli; trzeba też usunąć await, bo time.sleep nie jest awaitable.', 'No. It blocks the loop thread and is not awaitable.'),
    ('Co się zmieni bez return?', 'What if return is removed?', 'Funkcja zwróci domyślnie None zamiast 125.', 'The function implicitly returns None instead of 125.'),
    ('Co zrobi weather["missing"]?', 'What does weather["missing"] do?', 'Zgłosi KeyError. get("missing", wartość) pozwoli podać wartość domyślną.', 'Raises KeyError. get("missing", default) allows a fallback.'),
    ('Co zmieni await w zwykłej pętli po miastach?', 'What if you await each city in a normal loop?', 'Każdy odczyt zacznie się po poprzednim: około 4,5 s zamiast 1,5 s.', 'Each starts after the previous one: about 4.5 s instead of 1.5 s.'),
    ('Czy zmiana ziarna musi zmienić kolejność wyników?', 'Must changing the seed change result order?', 'Nie. Zmieni czasy, ale gather nadal oddaje wyniki według hosts.', 'No. Delays change, but gather still follows hosts order.'),
    ('Czy 404 jest tym samym co zerwane połączenie?', 'Is 404 the same as a failed connection?', 'Nie: 404 jest poprawnie odebraną odpowiedzią HTTP o braku zasobu.', 'No. 404 is a received HTTP response indicating a missing resource.'),
    ('Dlaczego wspólny czas nie wynosi 15 s?', 'Why is total time not 15 s?', 'Czekania 5,3,7 s nakładają się; decyduje najdłuższe.', 'The 5,3,7 s waits overlap; the longest dominates.'),
    ('Czy sum(jobs) zadziała przed gather?', 'Will sum(jobs) work before gather?', 'Nie. jobs zawiera korutyny, nie liczby; operacja dodawania zgłosi TypeError.', 'No. jobs contains coroutines rather than numbers; addition raises TypeError.'),
    ('Czy samo wait anuluje przegranych?', 'Does wait cancel the losers?', 'Nie. pending trzeba anulować i odebrać zakończenia.', 'No. Cancel pending tasks and await their completion.'),
    ('Co jeśli klient nie wyśle znaku nowej linii?', 'What if the client sends no newline?', 'readline może czekać; timeout klienta przerwie oczekiwanie.', 'readline may wait; the client timeout bounds the wait.'),
    ('Co jeśli pominiemy task_done?', 'What if task_done is omitted?', 'queue.join nie uzna pracy za skończoną i będzie czekać.', 'queue.join will not consider the work finished and will keep waiting.'),
    ('Co zrobi tryb w zamiast a?', 'What does mode w do instead of a?', 'Każde otwarcie utnie wcześniejszą treść, nawet gdy Lock poprawnie działa.', 'Each open truncates existing content even with a working Lock.'),
    ('Czy Semaphore(5) oznacza 5 zapytań na sekundę?', 'Does Semaphore(5) mean five requests per second?', 'Nie. Ogranicza liczbę równoczesnych operacji, a nie startów w jednostce czasu.', 'No. It limits concurrent operations, not starts per unit of time.'),
    ('Co jeśli komentarze pobierzemy po kolei?', 'What if comments are fetched sequentially?', 'Łączny czas będzie około 5 s: 1+1+1+1+1.', 'Total duration approaches 5 s: 1+1+1+1+1.'),
    ('Co bez raise po sprzątaniu w worker?', 'What if worker omits raise after cleanup?', 'Korutyna może zakończyć się zwyczajnie, a cancelled() zwróci False.', 'The coroutine can finish normally, with cancelled() returning False.'),
    ('Czy 100 pojawi się na liście?', 'Will 100 appear in the list?', 'Nie. 100 jest granicą, ale nie jest liczbą pierwszą. Ostatnia to 97.', 'No. 100 is the bound but is not prime; the last result is 97.'),
    ('Co zobaczysz dla opóźnienia 5 s i limitu 3 s?', 'What happens with delay 5 s and timeout 3 s?', 'Sprzątanie i Timeout=True, bez komunikatu sukcesu.', 'Cleanup and Timeout=True, without a success message.'),
]

PRESETS = {
    13: [('Wolny port / Free port', {'port': 0}), ('localhost:8888', {'port': 8888})],
    20: [('1 s · wynik / result', {'delay': 1}),
         ('5 s · timeout', {'delay': 5}), ('Losowo / Random 1–5 s', {'delay': 'random'})],
}

CORE_METHODS = {
    2: 'asyncio.sleep', 3: 'asyncio.sleep', 4: 'asyncio.gather',
    5: 'asyncio.sleep', 6: 'get', 7: 'asyncio.gather',
    8: 'rng.uniform', 9: 'aiohttp.ClientSession', 10: 'range',
    11: 'sum', 12: 'asyncio.wait', 13: 'asyncio.start_server',
    14: 'asyncio.Queue', 15: 'asyncio.Lock', 16: 'loop.time',
    17: 'asyncio.gather', 18: 'task.cancel', 19: 'all',
    20: 'asyncio.wait_for',
}


def method_detail(call, source):
    name = ast.unparse(call.func)
    short = name.rsplit('.', 1)[-1]
    note = METHODS.get(name) or INFRASTRUCTURE.get(name)
    note = note or METHODS.get(short) or INFRASTRUCTURE.get(short)
    if not note:
        return None
    return dict(start=call.lineno, end=call.end_lineno, body=pair(note),
                name=name, expression=ast.get_source_segment(source, call),
                arguments=[{'name': f'#{i}', 'value': ast.unparse(value)}
                           for i, value in enumerate(call.args, 1)] +
                          [{'name': value.arg or '**', 'value': ast.unparse(value.value)}
                           for value in call.keywords])


def lesson(number):
    if not 1 <= number <= 20:
        raise ValueError('Unknown task')
    record = json.loads((ROOT / 'material.json').read_text(encoding='utf-8'))[number - 1]
    path = ROOT / 'examples' / f'task{number:02}.py'
    source = path.read_text(encoding='utf-8')
    if source != record['source']:
        raise ValueError(f'Review explanations after changing {path.name}')
    tree = ast.parse(source)
    nodes = {n.name: n for n in ast.walk(tree)
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    steps = []
    for step in record['steps']:
        node = nodes[step['id']]
        actual = '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno])
        if actual != step['code'] or (node.lineno, node.end_lineno) != (step['start'], step['end']):
            raise ValueError(f'Invalid reviewed range: {number}.{step["id"]}')
        details = []
        if not isinstance(node, ast.ClassDef):
            seen = set()
            for call in sorted((n for n in ast.walk(node) if isinstance(n, ast.Call)),
                               key=lambda n: (n.lineno, n.col_offset)):
                name = ast.unparse(call.func)
                detail = method_detail(call, source)
                if detail and name not in seen:
                    details.append(detail)
                    seen.add(name)
        steps.append(dict(id=step['id'], start=node.lineno, end=node.end_lineno,
                          body=bilingual(step['body']), details=details,
                          name=step['id']))
    entry = next(n for n in tree.body if isinstance(n, ast.If))
    steps.insert(0, dict(id='entry', name='__main__ → run → main',
                         start=entry.lineno, end=entry.end_lineno, details=[],
                         body=bilingual('Od tego miejsca zaczyna się uruchomienie pliku. Warunek __name__ == "__main__" chroni przed startem przy imporcie. launch dodaje pomiar i zdarzenia. lambda options to mała funkcja przekazana do launch. W jej środku main() tworzy korutynę, a asyncio.run uruchamia ją we własnej pętli zdarzeń i sprząta pętlę po zakończeniu. Czytaj więc kod od wejścia do main, potem do wywoływanych funkcji.|Execution starts here. The __name__ guard prevents startup on import. launch adds timing and events. lambda options is a small function passed to launch. Within it main() creates a coroutine; asyncio.run executes it in its own event loop and cleans up afterwards. Read from this entry into main, then into called functions.')))
    data = {key: bilingual(record[key]) for key in
            ('title', 'intro', 'watch', 'takeaway', 'caveat', 'question', 'answer')}
    qpl, qen, apl, aen = EXPERIMENTS[number - 1]
    data.update(number=number, extra_question={'pl': qpl, 'en': qen},
                extra_answer={'pl': apl, 'en': aen},
                presets=[dict(label=label, value=value) for label, value in
                         PRESETS.get(number, [('Pokaz / Demo', {})])],
                assignment=assignment(number, bilingual(record['adaptation'])),
                steps=dict(file=path.name, source=source, steps=steps),
                terms=[dict(name='async def / await', body=bilingual(
                    'async def definiuje funkcję korutyny. Jej wywołanie tworzy obiekt korutyny. await odbiera wynik obiektu awaitable i może zawiesić bieżącą korutynę. Inne zadania postępują, gdy pętla odzyskuje sterowanie.|async def defines a coroutine function. Calling it creates a coroutine object. await retrieves an awaitable result and may suspend the current coroutine. Other tasks progress when the loop regains control.')),
                       dict(name='Dane → działanie → wynik / Input → work → result',
                            body=data['takeaway'])])
    if number in CORE_METHODS:
        method = CORE_METHODS[number]
        data['terms'][0] = dict(name=method, body=pair(METHODS[method]))
    return data
