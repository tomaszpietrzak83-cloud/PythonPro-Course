// TASK 01
const translations = {
    pl: {
        lesson: 'LEKCJA 29',
        sidebarTitle: 'Zrozum pracę w tle.',
        sidebarText: 'Uruchom. Zobacz kod. Poznaj mechanizm.',
        taskName: 'Pierwsze zadanie',
        scope: 'Pierwsza wersja · 1 z 20 zadań',
        workspace: 'PRACOWNIA',
        taskLabel: 'ZADANIE 01 · PODSTAWY',
        heading: 'Twoje pierwsze zadanie<br>w tle.',
        lead: 'Jedno kliknięcie, dwa procesy. Sprawdź, jak Django przekazuje pracę do Celery, a worker wykonuje ją poza żądaniem.',
        resultNode: '④ Wynik',
        experiment: 'EKSPERYMENT',
        demoTitle: 'Powiedz hello z workera',
        demoText: 'Zadanie wypisuje „Hello from Celery!” w konsoli workera. Zwraca też ten tekst, aby pokazać wynik na stronie.',
        run: 'Uruchom zadanie ↗',
        ready: 'Gotowe do uruchomienia',
        understand: 'ZROZUM KOD',
        studyTitle: 'Od kliknięcia do wyniku',
        fullCode: 'Pokaż pełny kod',
        guidedCode: 'Wróć do kroków',
        prev: '← Wstecz',
        next: 'Dalej →',
        checkLabel: 'OPCJONALNIE · SPRAWDŹ ZROZUMIENIE',
        checkTitle: 'Zatrzymaj się na chwilę',
        checkText: 'Spróbuj odpowiedzieć, zanim rozwiniesz wyjaśnienie.',
        footer: 'Celery Lab · ucz się na działającym kodzie · lekcja 29',
        waiting: 'Zadanie w kolejce / oczekiwanie na wynik',
        started: 'Worker wykonuje zadanie',
        success: 'Zadanie zakończone',
        failed: 'Zadanie nie powiodło się',
        offline: 'Nie udało się połączyć. Sprawdź serwer, Redis i workera.',
        timeout: 'Brak wyniku po 4 minutach. Zadanie może nadal czekać w kolejce. Sprawdź konsolę workera.',
        step: 'KROK'
    },
    en: {
        lesson: 'LESSON 29',
        sidebarTitle: 'Understand background work.',
        sidebarText: 'Run it. Read the code. Learn the mechanism.',
        taskName: 'Your first task',
        scope: 'First version · 1 of 20 tasks',
        workspace: 'WORKSPACE',
        taskLabel: 'TASK 01 · FUNDAMENTALS',
        heading: 'Your first task<br>in the background.',
        lead: 'One click, two processes. See how Django hands work to Celery and the worker executes it outside the HTTP request.',
        resultNode: '④ Result',
        experiment: 'EXPERIMENT',
        demoTitle: 'Say hello from the worker',
        demoText: 'The task prints “Hello from Celery!” in the worker console. It also returns the text so this page can display the result.',
        run: 'Run task ↗',
        ready: 'Ready to run',
        understand: 'UNDERSTAND THE CODE',
        studyTitle: 'From click to result',
        fullCode: 'Show full code',
        guidedCode: 'Back to walkthrough',
        prev: '← Previous',
        next: 'Next →',
        checkLabel: 'OPTIONAL · CHECK YOUR UNDERSTANDING',
        checkTitle: 'Take a moment to reflect',
        checkText: 'Try answering before revealing the explanation.',
        footer: 'Celery Lab · learn from working code · lesson 29',
        waiting: 'Task queued / waiting for a result',
        started: 'The worker is executing the task',
        success: 'Task completed',
        failed: 'Task failed',
        offline: 'Connection failed. Check the server, Redis and worker.',
        timeout: 'No result after 4 minutes. The task may still be queued. Check the worker console.',
        step: 'STEP'
    }
};
Object.assign(translations.pl, {
    backIntro: '← Treść zadania i wprowadzenie',
    compareLabel: 'WIĘCEJ PRZYKŁADÓW · TA SAMA FUNKCJA',
    compareTitle: 'Jedna funkcja, wiele niezależnych zadań',
    compareText: 'Zleć trzy wywołania hello_world. Każde otrzyma własny identyfikator, ale każde zwróci ten sam tekst. Poniżej pozostaje historia także pojedynczych kliknięć.',
    runThree: 'Zleć 3 zadania',
    compareNote: 'Historia pokazuje to, co zaobserwowała przeglądarka. To nie pomiar czasu pracy workera. Zadanie jest bardzo szybkie: stan STARTED może nie zostać zauważony. Worker solo wykonuje zadania pojedynczo.',
    execution: 'Wywołanie',
    sent: 'Kliknięcie → żądanie do Django',
    accepted: 'Django odpowiedziało 202 → zadanie przyjęte',
    observed: 'Przeglądarka odczytała wynik z backendu',
    historyEmpty: 'Tu pojawią się Twoje wywołania.'
});
Object.assign(translations.en, {
    backIntro: '← Assignment and introduction',
    compareLabel: 'MORE EXAMPLES · THE SAME FUNCTION',
    compareTitle: 'One function, independent tasks',
    compareText: 'Submit three calls to hello_world. Each receives a unique identifier, but returns the same text. The history below also keeps individual clicks.',
    runThree: 'Submit 3 tasks',
    compareNote: 'The history shows browser observations, not worker execution time. This task is very fast: STARTED may not be observed. The solo worker executes tasks one at a time.',
    execution: 'Call',
    sent: 'Click → request to Django',
    accepted: 'Django responded 202 → task accepted',
    observed: 'The browser read the result from the backend',
    historyEmpty: 'Your calls will appear here.'
});
let steps = [{
    file: 0,
    needle: 'from celery import shared_task',
    also: ['@shared_task'],
    pl: ['Zwykła funkcja staje się zadaniem',
        'Import shared_task udostępnia dekorator. @shared_task rejestruje funkcję jako zadanie Celery, które może odebrać worker.',
        'Dekorator nie uruchamia zadania. Definiuje, co worker będzie mógł wykonać.'
    ],
    en: ['A function becomes a task',
        'Importing shared_task gives us the decorator. @shared_task registers the function as a Celery task that a worker can receive.',
        'The decorator does not run the task. It defines work the worker can perform.'
    ]
}, {
    file: 0,
    needle: 'def hello_world',
    pl: ['Co robi worker?',
        'Worker wykonuje hello_world: tworzy tekst, wypisuje go na wyjściu procesu i zwraca wynik. print(..., flush=True) od razu opróżnia bufor wyjścia.',
        'Launcher zapisuje wyjście print w .runtime/worker.log. return trafia do backendu wyników — to dwa różne miejsca.'
    ],
    en: ['What does the worker do?',
        'The worker executes hello_world: it creates the message, prints it to process output and returns it. flush=True immediately flushes the output buffer.',
        'The launcher captures print output in .runtime/worker.log. return goes to the result backend — two different destinations.'
    ]
}, {
    file: 1,
    lines: [],
    needle: 'def run_hello',
    span: 10,
    pl: ['Kliknięcie wysyła żądanie do Django',
        'Przycisk wysyła żądanie POST do /tasks/1/run/. Widok run_hello wywołuje hello_world.delay(), czyli publikuje wiadomość do kolejki.',
        'hello_world() wykonałoby funkcję w Django. hello_world.delay() przekazuje wykonanie workerowi.'
    ],
    en: ['A click sends a request to Django',
        'The button sends a POST request to /tasks/1/run/. The run_hello view calls hello_world.delay(), publishing a message to the queue.',
        'hello_world() would execute inside Django. hello_world.delay() delegates execution to a worker.'
    ]
}, {
    file: 1,
    lines: [],
    needle: '{"task_id": task.id',
    context: 'def run_hello',
    span: 1,
    pl: ['Django oddaje numer zadania',
        'Odpowiedź HTTP 202 zawiera task_id. To identyfikator pozwalający sprawdzić wynik. Django nie czeka tutaj na wykonanie funkcji.',
        'Przyjęcie zadania do kolejki nie oznacza, że zostało już zakończone.'
    ],
    en: ['Django returns a task identifier',
        'The HTTP 202 response contains task_id. This identifier lets us check the result. Django does not wait here for the function to finish.',
        'Accepting a task into a queue does not mean the task has finished.'
    ]
}, {
    file: 2,
    needle: 'app.config_from_object',
    also: ['app.autodiscover_tasks'],
    pl: ['Jak worker poznaje konfigurację?',
        'Aplikacja Celery ładuje ustawienia Django z prefiksem CELERY i automatycznie szuka tasks.py w zainstalowanych aplikacjach.',
        'Worker jest osobnym procesem. Musi znać ten sam broker i backend wyników co Django.'
    ],
    en: ['How does the worker find its configuration?',
        'The Celery app loads Django settings prefixed with CELERY and discovers tasks.py in installed Django applications.',
        'The worker is a separate process. It needs the same broker and result backend as Django.'
    ]
}, {
    file: 1,
    lines: [],
    needle: 'def task_status',
    span: 9,
    pl: ['Przeglądarka sprawdza wynik',
        'Strona okresowo pyta endpoint statusu. AsyncResult odczytuje stan z backendu wyników. Gdy stan to SUCCESS, interfejs pokazuje zwrócony tekst.',
        'PENDING może oznaczać zadanie oczekujące albo nieznany identyfikator. Nie jest potwierdzeniem, że worker działa.'
    ],
    en: ['The browser checks the result',
        'The page polls the status endpoint. AsyncResult reads the state from the result backend. When the state is SUCCESS, the UI displays the returned message.',
        'PENDING may mean a queued task or an unknown identifier. It does not confirm that a worker is running.'
    ]
}];
let questions = [{
    pl: ['Gdzie pojawi się tekst z print()?',
        'Na wyjściu procesu workera Celery, zapisywanym przez launcher w .runtime/worker.log. Tekst na stronie pochodzi z return i backendu wyników.'
    ],
    en: ['Where does the print() message appear?',
        'In the Celery worker process console. The text on this page comes from return and the result backend.'
    ]
}, {
    pl: ['Czym różni się hello_world() od hello_world.delay()?',
        'Pierwsze wywołanie wykonuje funkcję bezpośrednio w bieżącym procesie. Drugie publikuje zadanie do brokera i zwraca AsyncResult z identyfikatorem.'
    ],
    en: ['How do hello_world() and hello_world.delay() differ?',
        'The first executes directly in the current process. The second publishes a task to the broker and returns AsyncResult with an identifier.'
    ]
}, {
    pl: ['Co się stanie, jeśli Redis działa, ale worker jest wyłączony?',
        'Django może przyjąć zadanie, ale żaden worker go nie odbierze. Zadanie pozostanie w kolejce do uruchomienia odpowiedniego workera.'
    ],
    en: ['What happens if Redis is running but the worker is stopped?',
        'Django can accept the task, but no worker consumes it. It remains queued until a suitable worker starts.'
    ]
}, {
    pl: ['Czy odpowiedź HTTP 202 oznacza sukces zadania?',
        'Nie. Oznacza przyjęcie żądania. Sukces wykonania potwierdza stan SUCCESS odczytany z backendu wyników.'
    ],
    en: ['Does HTTP 202 mean the task succeeded?',
        'No. It means the request was accepted. Successful execution is confirmed by SUCCESS in the result backend.'
    ]
}];
