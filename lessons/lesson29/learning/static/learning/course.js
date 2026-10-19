const sectionOrder = ['intro', 'examples', 'solution', 'code', 'questions'];
const labels = {
    pl: {
        intro: 'Wstęp',
        examples: 'Przykłady zastosowania',
        solution: 'Rozwiązanie krok po kroku',
        code: 'Cały kod',
        questions: 'Pytania',
        slides: 'Slajdy',
        continuous: 'Tryb ciągły',
        previous: '← Wstecz',
        next: 'Dalej →',
        goQuestions: 'Przejdź do pytań →',
        finish: 'Zakończ zadanie ✓',
        finished: 'Zadanie 1 ukończone',
        page: 'Strona',
        go: 'Przejdź do:',
        answer: 'Odkryj odpowiedź',
        summary: 'Podsumowanie rozwiązania',
        summaryText: 'Django publikuje zadanie przez .delay(). Broker przekazuje wiadomość workerowi. Worker wykonuje funkcję, a backend przechowuje wynik. Przeglądarka odczytuje wynik przez endpoint statusu.',
        reference: 'To sekcja referencyjna. Wybierz plik, aby zobaczyć aktualny kod aplikacji.',
        optional: 'Pytania są opcjonalne. Spróbuj odpowiedzieć przed odkryciem wyjaśnienia.',
        history: 'Historia Twoich wywołań',
        historyHint: 'Każde wywołanie ma własne task_id. Czasy dotyczą obserwacji przeglądarki, nie czasu wykonania funkcji.',
        historyButton: 'Zobacz historię →',
        empty: 'Najpierw uruchom zadanie na poprzedniej stronie.',
        single: 'Uruchom zadanie ↗',
        three: 'Zleć 3 zadania',
        backStart: 'Wróć do wstępu'
    },
    en: {
        intro: 'Introduction',
        examples: 'Use cases',
        solution: 'Step-by-step solution',
        code: 'Full code',
        questions: 'Questions',
        slides: 'Slides',
        continuous: 'Continuous',
        previous: '← Previous',
        next: 'Next →',
        goQuestions: 'Go to questions →',
        finish: 'Finish task ✓',
        finished: 'Task 1 completed',
        page: 'Page',
        go: 'Go to:',
        answer: 'Reveal the answer',
        summary: 'Solution summary',
        summaryText: 'Django publishes a task with .delay(). The broker passes the message to a worker. The worker executes the function and the backend stores the result. The browser reads the result through the status endpoint.',
        reference: 'This is a reference section. Select a file to inspect the actual application code.',
        optional: 'Questions are optional. Try answering before revealing the explanation.',
        history: 'Your execution history',
        historyHint: 'Each call has its own task_id. Times describe browser observations, not function execution time.',
        historyButton: 'View history →',
        empty: 'First run a task on the previous page.',
        single: 'Run task ↗',
        three: 'Submit 3 tasks',
        backStart: 'Back to introduction'
    }
};
const introPages = window.taskIntroduction || [{
    pl: ['Treść zadania',
        'Stwórz w pliku tasks.py proste zadanie o nazwie hello_world, które drukuje w konsoli workera napis:',
        'Stwórz widok Django, który po wejściu na odpowiedni URL wywoła to zadanie.',
        'W naszej aplikacji stronę otwierasz przez URL, a przycisk zleca zadanie przez POST. Odświeżenie strony nie zleca kolejnej pracy.'
    ],
    en: ['The assignment',
        'Create a simple task called hello_world in tasks.py that prints this message in the worker console:',
        'Create a Django view that triggers the task when its URL is accessed.',
        'In this app you open the page through its URL, then submit work with POST using a button. Refreshing does not enqueue more work.'
    ]
}, {
    pl: ['Co to znaczy: zadanie w tle?',
        'Zwykle Django wykonuje kod widoku, a potem odpowiada przeglądarce. Jeśli operacja trwa długo, użytkownik musi czekać.',
        'Celery pozwala zlecić tę pracę osobnemu procesowi. Django może odpowiedzieć, zanim praca zostanie zakończona.',
        'Celery nie przyspiesza samej funkcji. W tym zadaniu wypisujemy tylko jedno zdanie — uczymy się mechanizmu, nie ciężkich obliczeń.'
    ],
    en: ['What is a background task?',
        'Normally Django executes a view before responding to the browser. If an operation takes a long time, the user waits.',
        'Celery delegates that work to a separate process. Django can respond before the work finishes.',
        'Celery does not speed up the function itself. This task only prints a sentence: it teaches the mechanism, not heavy computation.'
    ]
}, {
    pl: ['Kto za co odpowiada?',
        'Django zleca → broker przechowuje wiadomość → worker wykonuje funkcję.',
        'Django jest zlecającym. Broker to pośrednik, np. Redis. Worker to osobny proces Celery, który odbiera i wykonuje zadania.',
        'Samo uruchomienie serwera Django nie uruchamia workera. run_app.py uruchamia oba procesy oraz Redis.'
    ],
    en: ['Who does what?',
        'Django submits → the broker holds a message → a worker executes the function.',
        'Django is the producer. The broker is an intermediary such as Redis. The worker is a separate Celery process that consumes and executes tasks.',
        'Starting Django alone does not start a worker. run_app.py starts both processes and Redis.'
    ]
}, {
    pl: ['Zlecenie a wynik',
        'task_id jest numerem zadania. Odpowiedź HTTP 202 mówi, że Django przyjęło zlecenie, ale nie potwierdza jego zakończenia.',
        'print() wypisuje tekst w konsoli workera. return oddaje wynik do backendu wyników, skąd może go odczytać strona.',
        'hello_world jest bardzo szybkie. Możesz zobaczyć od razu SUCCESS, bez zauważenia STARTED. To prawidłowe zachowanie.'
    ],
    en: ['Submission versus result',
        'task_id identifies a task. HTTP 202 means Django accepted the submission; it does not confirm completion.',
        'print() writes to the worker console. return sends a result to the result backend, where the page can read it.',
        'hello_world is very fast. You may see SUCCESS without observing STARTED. This is expected.'
    ]
}];
let language = localStorage.getItem('lesson29-language') === 'en' ? 'en' : 'pl';
let mode = localStorage.getItem('lesson29-mode') === 'continuous' ?
    'continuous' : 'slides';
let section = 'intro',
    page = 0,
    selectedFile = 0,
    busy = false;
const executionHistory = [];
const stage = document.getElementById('course-stage');
const sourceFiles = [...document.querySelectorAll('#source-files pre')].map(
    pre => ({
        name: pre.dataset.name,
        lines: pre.querySelector('code').innerHTML.replace(/\n$/, '')
            .split('\n')
    }));
const counts = {
    intro: introPages.length,
    examples: 3,
    solution: steps.length,
    code: 1,
    questions: questions.length
};
const text = key => labels[language][key];
Object.assign(labels.pl, {
    nextTask: 'Następne zadanie →',
    backList: 'Wróć do listy zadań'
});
Object.assign(labels.en, {
    nextTask: 'Next task →',
    backList: 'Back to the task list'
});
Object.assign(translations.pl, {
    invalid_numbers: 'Podaj dwie liczby od −10¹² do 10¹².'
});
Object.assign(translations.pl, {
    expected_failure: 'Oczekiwany FAILURE: wyczerpano 3 ponowienia',
    retry: 'Ponowienie za 60 s',
    progress: 'W trakcie',
    invalid_input: 'Sprawdź poprawność danych.'
});
Object.assign(translations.en, {
    expected_failure: 'Expected FAILURE: 3 retries exhausted',
    retry: 'Retry after 60 s',
    progress: 'In progress',
    invalid_input: 'Check your input.'
});
Object.assign(translations.en, {
    invalid_numbers: 'Enter two numbers between −10¹² and 10¹².'
});

function element(tag, content, className) {
    const node = document.createElement(tag);
    if (content !== undefined) node.textContent = content;
    if (className) node.className = className;
    return node;
}

function paragraph(parent, content, className) {
    parent.append(element('p', content, className));
}

function makePage(group, index, title) {
    const article = element('article', undefined, 'course-page panel');
    article.dataset.section = group;
    article.dataset.page = index;
    article.id = `${group}-${index}`;
    article.append(element('p',
        `${String(window.taskNumber).padStart(2,"0")} / ${text(group)} / ${index+1}`,
        'eyebrow'), element('h1', title));
    return article;
}

function button(title, callback, className = 'primary') {
    const node = element('button', title, className);
    node.type = 'button';
    node.onclick = callback;
    return node;
}

function editor(fileIndex, chosen = []) {
    const file = sourceFiles[fileIndex];
    const root = element('div', undefined, 'editor');
    const top = element('div', file.name, 'editor-top');
    root.append(top);
    const scroll = element('div', undefined, 'code-scroll');
    const pre = element('pre', undefined, 'code-file'),
        code = element('code');
    file.lines.forEach((html, index) => {
        const row = element('span', undefined, 'code-line');
        const content = element('span', undefined, 'code-text');
        content.innerHTML = html || ' ';
        row.append(content);
        if (chosen.length) row.classList.add(chosen.includes(index +
            1) ? 'focus' : 'dim');
        code.append(row);
    });
    pre.append(code);
    scroll.append(pre);
    root.append(scroll);
    return root;
}

function selectedLines(item) {
    if (!item.needle) return item.lines || [];
    const needle = item.needle.replace(/\s+/g, '');
    let ranges = JSON.parse(document.getElementById('code-ranges').textContent)[item.file];
    if(item.context){const scope=ranges.find(range=>range.text.startsWith(item.context.replace(/\s+/g,'')));if(!scope)throw new Error('Missing code scope: '+item.context);ranges=ranges.filter(range=>range.start>=scope.start&&range.end<=scope.end);}
    const prefix = ranges.filter(range => range.text.startsWith(needle));
    const candidates = prefix.length ? prefix : ranges.filter(range => range.text.includes(needle));
    candidates.sort((a, b) => (a.end - a.start) - (b.end - b.start));
    if (!candidates.length) throw new Error('Missing code fragment: ' + item.needle);
    const match = candidates[0];
    const lines=Array.from({length:match.end-match.start+1},(_,index)=>match.start+index);for(const needle of item.also||[])lines.push(...selectedLines({...item,needle,also:[]}));return [...new Set(lines)];
}

function build() {
    const oldScroll = stage.scrollTop;
    stage.replaceChildren();
    document.documentElement.lang = language;
    document.title =
        `Celery Lab · ${language==='pl'?'Zadanie':'Task'} ${window.taskNumber}`;
    document.querySelectorAll('[data-section]').forEach(node => {
        node.textContent = text(node.dataset.section);
    });
    document.querySelectorAll('[data-label]').forEach(node => node.textContent =
        text(node.dataset.label));
    document.getElementById('pl').setAttribute('aria-pressed', language ===
        'pl');
    document.getElementById('en').setAttribute('aria-pressed', language ===
        'en');
    document.getElementById('pl').classList.toggle('active', language === 'pl');
    document.getElementById('en').classList.toggle('active', language === 'en');
    introPages.forEach((item, index) => {
        const content = item[language],
            article = makePage('intro', index, content[0]);
        paragraph(article, content[1]);
        if (index === 0) article.append(element('pre', window
            .taskLesson ? window.taskLesson.sample : window
            .taskNumber === 2 ? 'multiply(a, b) → a * b' :
            'Hello from Celery!', 'assignment-code'));
        if (index === 2) article.append(element('div',
            `Django → ${window.lessonBroker} → Celery worker → ${language==='pl'?'wynik':'result'}`,
            'flow'));
        paragraph(article, content[2]);
        paragraph(article, content[3], 'note');
        stage.append(article);
    });
    if (window.taskNumber === 2) buildMultiplyExamples();
    else if (window.taskNumber > 2) buildExtendedExamples();
    else buildExamples();
    steps.forEach((item, index) => {
        const content = item[language],
            article = makePage('solution', index, content[0]);
        const layout = element('div', undefined, 'course-study');
        layout.append(editor(item.file, selectedLines(item)));
        const explanation = element('div', undefined, 'explanation');
        paragraph(explanation, content[1]);
        paragraph(explanation, content[2], 'note');
        layout.append(explanation);
        article.append(layout);
        if (index === steps.length - 1) {
            const cta = element('div', undefined, 'screen-cta');
            cta.append(button(text('goQuestions'), () => navigate(
                'questions', 0)));
            article.append(cta);
        }
        stage.append(article);
    });
    const full = makePage('code', 0, text('summary'));
    full.classList.add('full-code-page');
    paragraph(full, window.taskLesson ? window.taskLesson[language] : text(
        'summaryText'));
    paragraph(full, text('reference'), 'muted');
    const fullLayout = element('div', undefined, 'full-code-layout');
    const choices = element('div', undefined, 'file-choices');
    sourceFiles.forEach((file, index) => {
        const choice = button(file.name, () => {
            selectedFile = index;
            build();
        }, 'secondary');
        choice.classList.toggle('active', index === selectedFile);
        choices.append(choice);
    });
    const selectedSource = sourceFiles[selectedFile];
    const readmeHighlights = [];
    if (selectedSource.name === 'README.md') {
        const marker = new RegExp('(?:#|//)\\s*TASK\\s+0*' + window.taskNumber + '\\b');
        selectedSource.lines.forEach((html, index) => {
            const line = document.createElement('span');
            line.innerHTML = html;
            if (marker.test(line.textContent)) readmeHighlights.push(index + 1);
        });
    }
    fullLayout.append(choices, editor(selectedFile, readmeHighlights));
    full.append(fullLayout);
    stage.append(full);
    questions.forEach((question, index) => {
        const content = question[language],
            article = makePage('questions', index, content[0]);
        article.classList.add('course-question');
        paragraph(article, text('optional'));
        const details = element('details'),
            summary = element('summary', text('answer'));
        details.append(summary, element('p', content[1]));
        article.append(details);
        if (index === questions.length - 1) {
            const actions = element('div', undefined, 'finish-actions');
            if (window.taskNumber < 20) {
                const next = element('a', text('nextTask'), 'primary');
                next.href = `/tasks/${window.taskNumber+1}/`;
                actions.append(next);
            }
            const home = element('a', text('backList'), 'secondary');
            home.href = '/';
            actions.append(home);
            article.append(actions);
        }
        stage.append(article);
    });
    applyView(false);
    if (mode === 'continuous') stage.scrollTop = oldScroll;
    renderExecutions();
    translateNavigation();
}

function buildExamples() {
    const pl = language === 'pl';
    const first = makePage('examples', 0, pl ? 'Po co zlecać pracę do tła?' :
        'Why delegate work to the background?');
    paragraph(first, pl ?
        'Powitalny mail, generowanie raportu lub przetwarzanie zdjęcia mogą trwać długo. Django może zlecić operację i pozwolić użytkownikowi dalej korzystać ze strony.' :
        'A welcome email, report generation or image processing can take time. Django can delegate the operation and let the user keep using the page.'
        );
    paragraph(first, pl ?
        'To przykłady zastosowania Celery, nie dodatkowe funkcje zadania 1. Tutaj worker tylko wypisuje „Hello from Celery!”.' :
        'These are Celery use cases, not additional features of task 1. Here the worker only prints “Hello from Celery!”.',
        'note');
    paragraph(first, translations[language].demoText);
    const actions = element('div', undefined, 'example-actions');
    const run = button(text('single'), () => runExamples(1));
    run.dataset.run = '1';
    run.disabled = busy;
    actions.append(run);
    first.append(actions, makeOutput());
    stage.append(first);
    const second = makePage('examples', 1, pl ? 'Jedna funkcja, trzy zlecenia' :
        'One function, three submissions');
    paragraph(second, pl ?
        'Zleć trzy niezależne wywołania tej samej funkcji. Każde dostanie inny task_id, choć wszystkie zwrócą ten sam tekst.' :
        'Submit three independent calls of the same function. Each gets a different task_id, although all return the same text.'
        );
    paragraph(second, pl ?
        'Worker solo wykonuje zadania pojedynczo. Trzy wywołania nie oznaczają trzech workerów ani równoległej pracy.' :
        'The solo worker executes tasks one at a time. Three calls do not mean three workers or parallel execution.',
        'note');
    const three = button(text('three'), () => runExamples(3));
    three.dataset.run = '3';
    three.disabled = busy;
    second.append(three, makeOutput());
    stage.append(second);
    const third = makePage('examples', 2, text('history'));
    paragraph(third, text('historyHint'));
    const history = element('div', undefined, 'course-history');
    history.id = 'execution-history';
    history.setAttribute('aria-live', 'polite');
    third.append(history);
    stage.append(third);
}

function makeOutput() {
    const output = element('div', undefined, 'example-output');
    output.setAttribute('role', 'status');
    output.setAttribute('aria-live', 'polite');
    return output;
}

function renderExecutions() {
    if (window.taskNumber === 18) renderParallelWorkers();
    const latest = executionHistory.at(-1);
    document.querySelectorAll('.example-output').forEach(root => {
        root.replaceChildren();
        root.append(element('strong', translations[language][latest
            ?.state || 'ready'
        ] || latest?.state));
        if (latest?.expression) root.append(element('p', latest
            .expression));
        if (latest?.id) root.append(element('code',
            `task_id: ${latest.id}`));
        if (latest?.progress) {
            const progress = element('progress');
            progress.max = latest.progress.total;
            progress.value = latest.progress.current;
            root.append(progress, element('span',
                `${latest.progress.current} / ${latest.progress.total}`
                ));
        }
        if (latest?.result?.download_url) {
            const link = element('a', language === 'pl' ?
                'Pobierz plik' : 'Download file', 'secondary');
            link.href = latest.result.download_url;
            link.download = '';
            root.append(link);
        }
        if (latest?.result !== undefined) root.append(element('pre',
            typeof latest.result === 'object' ? JSON.stringify(
                latest.result, null, 2) : latest.result));
        if (executionHistory.length) root.append(button(text(
                'historyButton'), () => navigate('examples', 2),
            'secondary'));
    });
    const root = document.getElementById('execution-history');
    root.replaceChildren();
    if (!executionHistory.length) {
        paragraph(root, text('empty'));
        return;
    } [...executionHistory].reverse().forEach(record => {
        const card = element('article', undefined, 'execution-card');
        card.append(element('strong',
            `${translations[language].execution} ${record.number} · ${translations[language][record.state]}`
            ));
        if (record.expression) card.append(element('p', record
            .expression));
        if (record.id) card.append(element('code',
            `task_id: ${record.id}`));
        record.events.forEach(event => card.append(element('div',
            `${new Date(event.time).toLocaleTimeString(language==='pl'?'pl-PL':'en-GB')} · ${translations[language][event.key]}`,
            'history-event')));
        if (record.result !== undefined) card.append(element('pre',
            typeof record.result === 'object' ? JSON.stringify(
                record.result, null, 2) : record.result));
        root.append(card);
    });
}

function applyView(scroll = true) {
    document.body.classList.toggle('continuous', mode === 'continuous');
    document.getElementById('slides').classList.toggle('active', mode ===
        'slides');
    document.getElementById('continuous').classList.toggle('active', mode ===
        'continuous');
    document.getElementById('slides').setAttribute('aria-pressed', mode ===
        'slides');
    document.getElementById('continuous').setAttribute('aria-pressed', mode ===
        'continuous');
    document.querySelectorAll('.course-page').forEach(article => article
        .hidden = mode === 'slides' && (article.dataset.section !==
            section || Number(article.dataset.page) !== page));
    document.querySelectorAll('.course-menu button').forEach(node => {
        node.classList.toggle('active', node.dataset.section ===
            section);
        if (node.dataset.section === section) node.setAttribute(
            'aria-current', 'page');
        else node.removeAttribute('aria-current');
    });
    const previous = document.getElementById('previous'),
        next = document.getElementById('following');
    previous.textContent = text('previous');
    previous.disabled = section === 'intro' && page === 0;
    next.disabled = false;
    next.textContent = page < counts[section] - 1 ? text('next') : section ===
        'solution' ? text('goQuestions') : section === 'questions' ? text(window
            .taskNumber < 20 ? 'nextTask' : 'backList') :
        `${text('go')} ${text(sectionOrder[sectionOrder.indexOf(section)+1]||'intro')} →`;
    document.getElementById('page-counter').textContent =
        `${text(section)} · ${text('page')} ${page+1} / ${counts[section]}`;
    if (scroll) {
        const article = document.getElementById(`${section}-${page}`);
        if (mode === 'continuous') stage.scrollTo({
            top: article.offsetTop - stage.offsetTop - 22,
            behavior: 'instant'
        });
        else {
            stage.scrollTop = 0;
            article.scrollTop = 0;
            const focus = article.querySelector('.focus');
            if (focus) {
                const box = focus.closest('.code-scroll');
                box.scrollTop = Math.max(0, focus.offsetTop - focus.closest(
                    'pre').offsetTop - 50);
            }
        }
    }
}

function navigate(group, index = 0, updateHash = true) {
    if (!sectionOrder.includes(group)) return;
    section = group;
    page = Math.max(0, Math.min(counts[group] - 1, index));
    applyView();
    if (updateHash) window.history.replaceState(null, '',
        `#${section}/${page+1}`);
}

function nextPage() {
    if (page < counts[section] - 1) return navigate(section, page + 1);
    if (section === 'solution') return navigate('questions');
    if (section === 'questions') {
        location.href = window.taskNumber < 20 ?
            `/tasks/${window.taskNumber+1}/` : '/';
        return;
    }
    navigate(sectionOrder[sectionOrder.indexOf(section) + 1] || 'intro');
}

function previousPage() {
    if (page > 0) return navigate(section, page - 1);
    const previous = sectionOrder[sectionOrder.indexOf(section) - 1];
    if (previous) navigate(previous, counts[previous] - 1);
}
async function submitOne(args, taskNumber = window.taskNumber, onRecord = null) {
    const record = {
        number: executionHistory.length + 1,
        state: 'waiting',
        events: [{
            key: 'sent',
            time: Date.now()
        }]
    };
    if (args?.a !== undefined) record.expression = args.a + ' × ' + args.b;
    executionHistory.push(record);
    if (onRecord) onRecord(record);
    renderExecutions();
    try {
        const response = await fetch('/tasks/' + taskNumber +
            '/run/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector(
                        '[name=csrfmiddlewaretoken]').value
                },
                ...(args ? {
                    body: args instanceof FormData ? args :
                        new URLSearchParams(args)
                } : {})
            });
        if (!response.ok) {
            if (response.status === 400) {
                record.state = window.taskNumber === 2 ? 'invalid_numbers' :
                    'invalid_input';
                return;
            }
            throw Error('publish');
        }
        const submission = await response.json();
        if (submission.state === 'ROLLED_BACK') {
            record.state = 'success';
            record.result = submission.result;
            return;
        }
        record.id = submission.task_id;
        record.submissions = submission.submissions;
        if (submission.message) record.result = submission.message;
        record.events.push({
            key: 'accepted',
            time: Date.now()
        });
        renderExecutions();
        const deadline = Date.now() + 240000;
        while (Date.now() < deadline) {
            const response = await fetch(`/tasks/status/${record.id}/`);
            if (!response.ok) throw Error('status');
            const result = await response.json();
            if (record.submissions) {
                const batch = await Promise.all(record.submissions.map(
                async item => {
                        const r = await fetch(
                            `/tasks/status/${item.task_id}/`
                            );
                        return {
                            ...item,
                            ...await r.json()
                        };
                    }));
                record.progress = {
                    current: batch.filter(x => x.state === 'SUCCESS')
                        .length,
                    total: 50
                };
                record.result = batch;
                if (batch.some(x => x.state === 'FAILURE')) {
                    record.state = 'failed';
                    return;
                }
                if (record.progress.current === 50) {
                    record.state = 'success';
                    return;
                }
                renderExecutions();
                await new Promise(resolve => setTimeout(resolve, 1000));
                continue;
            }
            record.progress = result.progress;
            if (result.state === 'SUCCESS') {
                record.state = 'success';
                record.result = result.result;
                record.events.push({
                    key: 'observed',
                    time: Date.now()
                });
                return;
            }
            if (result.state === 'FAILURE') {
                record.state = window.taskNumber === 15 ?
                    'expected_failure' : 'failed';
                return;
            }
            record.state = result.state === 'RETRY' ? 'retry' : result
                .state === 'PROGRESS' ? 'progress' : result.state ===
                'STARTED' ? 'started' : 'waiting';
            renderExecutions();
            await new Promise(resolve => setTimeout(resolve, 650));
        }
        record.state = 'timeout';
    } catch (error) {
        record.state = 'offline';
    } finally {
        renderExecutions();
    }
}
async function runExamples(count, argumentsList = null) {
    if (busy) return;
    busy = true;
    document.querySelectorAll('[data-run]').forEach(node => node.disabled =
        true);
    try {
        await Promise.all(Array.from({
            length: count
        }, (_, index) => submitOne(argumentsList?.[index])));
    } finally {
        busy = false;
        document.querySelectorAll('[data-run]').forEach(node => node
            .disabled = false);
        renderExecutions();
    }
}
document.querySelectorAll('[data-section]').forEach(node => node.onclick = () =>
    navigate(node.dataset.section));
document.getElementById('previous').onclick = previousPage;
document.getElementById('following').onclick = nextPage;
for (const lang of ['pl', 'en']) document.getElementById(lang).onclick = () => {
    language = lang;
    localStorage.setItem('lesson29-language', language);
    build();
};
for (const choice of ['slides', 'continuous']) document.getElementById(choice)
    .onclick = () => {
        mode = choice;
        localStorage.setItem('lesson29-mode', mode);
        applyView();
    };

function readHash() {
    const match = location.hash.match(
        /^#(intro|examples|solution|code|questions)\/(\d+)$/);
    if (match) {
        section = match[1];
        page = Math.max(0, Math.min(counts[section] - 1, Number(match[2]) - 1));
    }
}
window.addEventListener('hashchange', () => {
    readHash();
    applyView();
});
let scrollPending = false;
stage.addEventListener('scroll', () => {
    if (mode !== 'continuous' || scrollPending) return;
    scrollPending = true;
    requestAnimationFrame(() => {
        scrollPending = false;
        const articles = [...stage.querySelectorAll(
            '.course-page')];
        const bounds = stage.getBoundingClientRect();
        const visible = articles.find(article => article
            .getBoundingClientRect().bottom > bounds.top +
            80);
        if (visible) {
            section = visible.dataset.section;
            page = Number(visible.dataset.page);
            applyView(false);
        }
    });
});
readHash();
build();
applyView();
