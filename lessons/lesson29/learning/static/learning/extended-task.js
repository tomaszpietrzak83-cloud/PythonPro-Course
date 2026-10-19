window.taskLesson = JSON.parse(document.getElementById('curriculum')
    .textContent);
window.taskIntroduction = window.taskLesson.intros;
steps = window.taskLesson.steps;
questions = window.taskLesson.questions;

function buildExtendedExamples() {
    if (window.taskNumber === 18) {
        buildParallelWorkersExamples();
        return;
    }
    const pl = language === 'pl',
        n = window.taskNumber;
    const first = makePage('examples', 0, pl ? 'Uruchom i obserwuj' :
        'Run and observe');
    paragraph(first, window.taskLesson[language]);
    const form = element('form', undefined, 'number-form exercise-form');

    function field(name, label, value, type = 'text') {
        const wrap = element('label', label);
        const input = element('input');
        input.name = name;
        input.type = type;
        if (type !== 'file') input.value = value;
        input.required = true;
        if (type === 'file') input.accept = 'image/*';
        wrap.append(input);
        form.append(wrap);
    }
    if (n === 7) field('user_id', pl ? 'ID użytkownika' : 'User ID', '1',
        'number');
    if (n === 10 || n === 18) {
        field('recipient_email', 'Email', 'student@example.com', 'email');
        field('subject', pl ? 'Temat' : 'Subject', 'Celery lesson');
        field('body', pl ? 'Treść' : 'Body', 'Hello from Celery!');
    }
    if (n === 16) field('image', pl ? 'Obraz (maks. 5 MB)' :
        'Image (max. 5 MB)', '', 'file');
    if (n === 20) field('text', pl ? 'Tekst do przetworzenia' :
        'Text to process', 'hello transaction');
    const run = button(n === 9 ? (pl ? 'Zleć 50 zadań' : 'Submit 50 tasks') :
        n === 19 ? (pl ? 'Zleć przez Flower' : 'Submit through Flower') :
        text('single'), () => {});
    run.type = 'submit';
    run.dataset.run = '1';
    run.disabled = busy;
    form.append(run);
    form.onsubmit = event => {
        event.preventDefault();
        runExamples(1, [new FormData(form)]);
    };
    first.append(form, makeOutput());
    if (n === 19) {
        const links = element('div', undefined, 'example-actions');
        for (const [label, path] of [
                ['Dashboard', '/'],
                ['Tasks', '/tasks'],
                ['Workers', '/workers']
            ]) {
            const a = element('a', label, 'secondary');
            a.href = 'http://127.0.0.1:5559' + path;
            a.target = '_blank';
            a.rel = 'noopener';
            links.append(a);
        }
        first.append(links);
    }
    stage.append(first);
    const second = makePage('examples', 1, pl ? 'Sprawdź dane i porównaj' :
        'Inspect and compare');
    paragraph(second, pl ?
        'Odczytaj aktualny stan pliku, bazy lub harmonogramu. Po wykonaniu zadania odśwież dane i porównaj je z poprzednim wynikiem.' :
        'Read the current file, database or schedule state. Refresh after execution and compare it with the previous result.'
        );
    const snapshot = element('div', pl ? 'Kliknij „Odśwież dane”.' :
        'Click “Refresh data”.', 'data-snapshot');
    snapshot.style.maxHeight = '45vh';
    snapshot.style.overflow = 'auto';
    const refresh = async () => {
        try {
            const response = await fetch(`/tasks/${n}/data/`);
            const data = await response.json();
            renderDataSnapshot(snapshot, data, pl);
        } catch {
            snapshot.textContent = translations[language].offline;
        }
    };
    second.append(button(pl ? 'Odśwież dane' : 'Refresh data', refresh,
        'secondary'), snapshot);
    if (n === 20) {
        paragraph(second, pl ?
            'Porównaj zatwierdzenie z wycofaniem: rollback nie zapisze rekordu i nie wyśle zadania.' :
            'Compare commit with rollback: rollback saves no record and publishes no task.'
            );
        const rollback = button(pl ? 'Przykład: rollback' : 'Example: rollback',
            () => runExamples(1, [{
                text: 'discard me',
                rollback: 'yes'
            }]), 'secondary');
        rollback.dataset.run = '1';
        second.append(rollback, makeOutput());
    }
    stage.append(second);
    const third = makePage('examples', 2, text('history'));
    paragraph(third, text('historyHint'));
    const history = element('div', undefined, 'course-history');
    history.id = 'execution-history';
    history.setAttribute('aria-live', 'polite');
    third.append(history);
    stage.append(third);
}

function renderDataSnapshot(root, data, pl) {
    root.replaceChildren();
    const names = {
        users: pl ? 'Użytkownicy' : 'Users',
        notifications: pl ? 'Powiadomienia' : 'Notifications',
        logs: pl ? 'Logi' : 'Logs',
        pages: pl ? 'Pobrane tytuły' : 'Fetched titles',
        images: pl ? 'Obrazy' : 'Images',
        records: pl ? 'Przetworzone rekordy' : 'Processed records',
        'log.txt': 'log.txt',
        id: 'ID',
        username: pl ? 'Użytkownik' : 'Username',
        email: 'Email',
        last_login: pl ? 'Ostatnie logowanie' : 'Last login',
        recipient_email: pl ? 'Odbiorca' : 'Recipient',
        subject: pl ? 'Temat' : 'Subject',
        body: pl ? 'Treść' : 'Body',
        sent_at: pl ? 'Data wysyłki' : 'Sent at',
        message: pl ? 'Treść' : 'Message',
        created_at: pl ? 'Data utworzenia' : 'Created at',
        url: 'URL',
        title: pl ? 'Tytuł' : 'Title',
        fetched_at: pl ? 'Pobrano' : 'Fetched at',
        image: pl ? 'Plik' : 'File',
        classification_result: pl ? 'Klasyfikacja' : 'Classification',
        text: pl ? 'Tekst' : 'Text',
        processed_at: pl ? 'Przetworzono' : 'Processed at'
    };
    if (!Object.keys(data).length) {
        paragraph(root, pl ?
            'Wynik tego zadania zobaczysz w historii wywołań.' :
            'View this task result in execution history.');
        return;
    }
    for (const [name, rows] of Object.entries(data)) {
        if (name === 'schedule') {
            paragraph(root, (pl ? 'Aktywny harmonogram: ' :
                'Active schedule: ') + ({
                    4: pl ? 'co 10 sekund' : 'every 10 seconds',
                    6: pl ? 'codziennie o 23:00' : 'daily at 23:00',
                    12: pl ? 'codziennie o 00:15' : 'daily at 00:15',
                    13: pl ? 'co godzinę, w minucie 00' :
                        'hourly, at minute 00'
                } [window.taskNumber]) + ' · ' + rows.timezone, 'note');
            continue;
        }
        root.append(element('h3', names[name] || name));
        if (!rows.length) {
            paragraph(root, pl ? 'Brak zapisanych danych.' : 'No saved data.');
            continue;
        }
        if (typeof rows[0] === 'string') {
            root.append(element('pre', rows.join('\n')));
            continue;
        }
        const table = element('table', undefined, 'data-table');
        const head = element('tr');
        const keys = Object.keys(rows[0]);
        keys.forEach(key => head.append(element('th', names[key] || key)));
        table.append(head);
        rows.forEach(row => {
            const tr = element('tr');
            keys.forEach(key => {
                let value = row[key];
                if (value === null || value === '') value = pl ?
                    'Oczekuje' : 'Pending';
                else if (/_at$|last_login/.test(key)) value =
                    new Date(value).toLocaleString(pl ?
                        'pl-PL' : 'en-GB');
                tr.append(element('td', String(value)));
            });
            table.append(tr);
        });
        root.append(table);
    }
}


const parallelWorkers = {
    video: {record: null, running: false},
    mail: {record: null, running: false}
};

function buildParallelWorkersExamples() {
    const pl = language === 'pl';
    const prep = makePage('examples', 0,
        pl ? 'Dwie kolejki, dwa workery' : 'Two queues, two workers');
    paragraph(prep, pl
        ? 'Na następnym slajdzie zobaczysz film i mail obok siebie. Film zajmie workera default przez około 15 sekund. Symulowany mail zajmie osobnego workera priority_queue przez około 2 sekundy.'
        : 'The next slide shows video and email side by side. Video occupies the default worker for about fifteen seconds. Simulated email occupies a separate priority_queue worker for about two seconds.');
    paragraph(prep, pl
        ? 'Kliknij „Zleć oba”. Dwa żądania zostaną wysłane równolegle. Obserwuj, czy mail zakończy się, gdy film nadal będzie przetwarzany. Możesz też zlecać zadania osobno.'
        : 'Click “Submit both”. Two requests are sent concurrently. Watch whether email finishes while video is still processing. You can also submit each task separately.');
    paragraph(prep, pl
        ? 'Statusy pochodzą z backendu Celery. Przyjęcie zlecenia nie oznacza rozpoczęcia pracy. Zajęta kolejka może opóźnić wykonanie; nazwa priority_queue sama nie nadaje priorytetu. Mail jest symulacją, bez prawdziwej wysyłki.'
        : 'Statuses come from the Celery backend. Acceptance does not mean execution has started. A busy queue can delay work; the name priority_queue alone does not assign priority. Email delivery is simulated.', 'note');
    prep.append(button(pl ? 'Przejdź do obserwacji →' : 'Observe the workers →',
        () => navigate('examples', 1)));
    stage.append(prep);

    const demo = makePage('examples', 1,
        pl ? 'Obserwuj dwa workery' : 'Watch two workers');
    demo.classList.add('parallel-workers-page');
    const both = button(pl ? 'Zleć oba' : 'Submit both',
        () => Promise.all([runParallelWorker('video'), runParallelWorker('mail')]));
    both.id = 'parallel-both';
    const toolbar = element('div', undefined, 'workers-toolbar');
    toolbar.append(demo.querySelector('h1'), both);
    demo.append(toolbar);
    const panels = element('div', undefined, 'parallel-workers');
    for (const kind of ['video', 'mail']) {
        const video = kind === 'video';
        const panel = element('section', undefined, 'worker-panel');
        panel.append(element('h2', video ? (pl ? 'Film · 15 s' : 'Video · 15 s')
            : (pl ? 'Mail · 2 s' : 'Email · 2 s')));
        paragraph(panel, video ? 'default' : 'priority_queue', 'worker-queue');
        const run = button(video ? (pl ? 'Zleć film' : 'Submit video')
            : (pl ? 'Zleć mail' : 'Submit email'), () => runParallelWorker(kind), 'secondary');
        run.id = 'parallel-run-' + kind;
        const status = element('div', undefined, 'worker-status');
        status.id = 'parallel-status-' + kind;
        status.setAttribute('role', 'status');
        status.setAttribute('aria-live', 'polite');
        panel.append(run, status);
        panels.append(panel);
    }
    demo.append(panels);
    stage.append(demo);
    const history = makePage('examples', 2, text('history'));
    paragraph(history, text('historyHint'));
    const records = element('div', undefined, 'course-history');
    records.id = 'execution-history';
    records.setAttribute('aria-live', 'polite');
    history.append(records);
    stage.append(history);
}

function renderParallelWorkers() {
    const pl = language === 'pl';
    for (const kind of ['video', 'mail']) {
        const state = parallelWorkers[kind];
        const root = document.getElementById('parallel-status-' + kind);
        if (!root) continue;
        const detailsOpen = root.querySelector('details')?.open || false;
        root.replaceChildren();
        const record = state.record;
        root.dataset.state = record?.state || 'ready';
        const labels = pl
            ? {ready: 'Gotowy', waiting: 'W kolejce', started: 'W trakcie', success: 'Zakończone'}
            : {ready: 'Ready', waiting: 'Queued', started: 'Running', success: 'Completed'};
        root.append(element('strong', labels[record?.state || 'ready']
            || translations[language][record?.state] || record?.state));
        if (record?.id) {
            const details = element('details', undefined, 'worker-details');
            details.open = detailsOpen;
            details.append(element('summary', pl ? 'ID i czasy' : 'ID and times'));
            details.append(element('code', 'task_id: ' + record.id));
            details.append(element('div', kind === 'video'
                ? 'lesson29-default' : 'lesson29-priority'));
            for (const event of record.events) {
                const labels = {sent: pl ? 'Żądanie' : 'Request',
                    accepted: pl ? 'Przyjęto' : 'Accepted',
                    observed: pl ? 'Wynik odebrany' : 'Result observed'};
                details.append(element('div', labels[event.key] + ' · '
                    + new Date(event.time).toLocaleTimeString(pl ? 'pl-PL' : 'en-GB'),
                    'worker-event'));
            }
            root.append(details);
        }
        document.getElementById('parallel-run-' + kind).disabled = state.running;
    }
    const both = document.getElementById('parallel-both');
    if (both) both.disabled = parallelWorkers.video.running || parallelWorkers.mail.running;
}

async function runParallelWorker(kind) {
    const state = parallelWorkers[kind];
    if (state.running) return;
    state.running = true;
    renderParallelWorkers();
    try {
        await submitOne(kind === 'mail' ? {
            recipient_email: 'student@example.com',
            subject: 'Two workers demonstration',
            body: 'Hello from Celery!'
        } : null, kind === 'video' ? 8 : 18, record => {
            record.expression = kind === 'video'
                ? 'Film / Video · default' : 'Mail / Email · priority_queue';
            state.record = record;
        });
    } finally {
        state.running = false;
        renderParallelWorkers();
    }
}
