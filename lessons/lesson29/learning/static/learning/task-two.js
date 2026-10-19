// TASK 02
window.taskIntroduction = [{
    pl: ['Treść zadania',
        'Napisz zadanie multiply(a, b), które przyjmuje dwie liczby i zwraca ich iloczyn.',
        'W widoku stwórz prosty formularz HTML z dwoma polami. Pobierz z nich liczby i przekaż je do zadania Celery.',
        'Cel ćwiczenia: przekazać argumenty do workera i odebrać wynik. Kod mnożenia nadal wykona się poza procesem Django.'
    ],
    en: ['The assignment',
        'Write a task multiply(a, b) that receives two numbers and returns their product.',
        'Create a simple HTML form with two fields in the view. Read the numbers and pass them to the Celery task.',
        'Goal: send arguments to the worker and receive a result. The multiplication still executes outside the Django process.'
    ]
}, {
    pl: ['Argumenty: dane dla zadania',
        'W zadaniu 1 funkcja nie potrzebowała danych wejściowych. Teraz musi wiedzieć, jakie dwie liczby pomnożyć.',
        'multiply.delay(6, 7) przekazuje do kolejki nazwę zadania oraz argumenty 6 i 7. Worker wywoła multiply(6, 7).',
        'Przekazujemy proste liczby. Nie przekazujemy całego formularza ani obiektu request.'
    ],
    en: ['Arguments: task input',
        'Task 1 needed no input. Now the function needs to know which two numbers to multiply.',
        'multiply.delay(6, 7) sends the task name and arguments 6 and 7 to the queue. The worker will call multiply(6, 7).',
        'We pass simple numbers, not the entire form or request object.'
    ]
}, {
    pl: ['Formularz a liczby',
        'Przeglądarka wysyła pola formularza jako tekst. Django odczytuje je z request.POST i zamienia na liczby.',
        'Walidacja odrzuca puste pola, wartości nieliczbowe i liczby poza zakresem ćwiczenia. Dopiero poprawne dane trafiają do Celery.',
        'Używamy float, więc obsługujemy również ułamki. float może zaokrąglać: nie jest dobrym wyborem do precyzyjnych rozliczeń pieniędzy.'
    ],
    en: ['Form fields versus numbers',
        'The browser sends form fields as text. Django reads request.POST and converts the values to numbers.',
        'Validation rejects missing, nonnumeric and out-of-range values. Only valid inputs are sent to Celery.',
        'We use float to support fractional numbers. float can round values: it is not appropriate for precise financial accounting.'
    ]
}, {
    pl: ['Wynik jest oddzielny od zlecenia',
        'Django zwraca task_id, a nie natychmiastowy wynik mnożenia. Worker liczy iloczyn i zapisuje go w backendzie wyników.',
        'Strona pyta o status, a po SUCCESS pokazuje wynik, np. 6 × 7 = 42. Każde kliknięcie tworzy nowe zadanie.',
        'Wynik 0 również jest poprawnym wynikiem. Nie należy mylić zera z brakiem wyniku.'
    ],
    en: ['The result is separate from submission',
        'Django returns task_id rather than an immediate product. The worker calculates the product and stores it in the result backend.',
        'The page checks the status and displays the result after SUCCESS, for example 6 × 7 = 42. Each click creates a new task.',
        'Zero is also a valid result. Do not confuse zero with a missing result.'
    ]
}];
steps = [{
    file: 0,
    lines: [],
    needle: 'def multiply',
    span: 3,
    pl: ['Funkcja przyjmuje argumenty',
        'multiply(a, b) otrzymuje dwie liczby. Dekorator @shared_task nad funkcją rejestruje ją jako zadanie Celery.',
        'Nazwy a i b są parametrami funkcji. Konkretne wartości przekażemy przy wywołaniu .delay().'
    ],
    en: ['The function receives arguments',
        'multiply(a, b) receives two numbers. @shared_task above the function registers it as a Celery task.',
        'a and b are parameters. We will pass concrete values when calling .delay().'
    ]
}, {
    file: 0,
    lines: [],
    needle: 'return a * b',
    span: 1,
    pl: ['Worker oblicza iloczyn',
        'return a * b mnoży argumenty i oddaje wynik. Dla a=6 i b=7 wynikiem jest 42.',
        'W przeciwieństwie do zadania 1 nie potrzebujemy print(). Wynik pochodzi z return.'
    ],
    en: ['The worker calculates the product',
        'return a * b multiplies the arguments and returns the result. For a=6 and b=7, the result is 42.',
        'Unlike task 1, print() is not needed. The result comes from return.'
    ]
}, {
    file: 1,
    context: 'def run_multiply',
    lines: [],
    needle: 'a = float',
    also: ['b = float'],
    span: 6,
    pl: ['Django odczytuje pola formularza',
        'Widok run_multiply przyjmuje POST. request.POST.get pobiera tekst z pól a i b, a float zamienia go na liczbę.',
        'Formularz ma dokładnie dwa pola liczbowe. Jego kod znajdziesz w pliku task-two.js w zakładce Cały kod.'
    ],
    en: ['Django reads the form fields',
        'The run_multiply view accepts POST. request.POST.get reads text from a and b, and float converts it into a number.',
        'The form has two numeric fields. Its implementation is in task-two.js under Full code.'
    ]
}, {
    file: 1,
    context: 'def run_multiply',
    lines: [],
    needle: 'if not all(math.isfinite',
    also: ['return JsonResponse({"error": "invalid_numbers"'],
    span: 5,
    pl: ['Walidacja przed zleceniem',
        'Sprawdzamy, czy wartości są skończone i mieszczą się w zakresie ćwiczenia. Niepoprawne dane kończą się odpowiedzią 400.',
        'Nie zlecamy workerowi zadania, jeśli formularz zawiera niepoprawne dane. Walidacja przeglądarki jest tylko dodatkowym ułatwieniem.'
    ],
    en: ['Validate before submission',
        'We check that values are finite and within the exercise range. Invalid input receives HTTP 400.',
        'We do not enqueue invalid input. Browser validation is only an additional convenience.'
    ]
}, {
    file: 1,
    context: 'def run_multiply',
    lines: [],
    needle: 'task = multiply.delay(a, b)',
    also: ['return JsonResponse({"task_id": task.id'],
    span: 4,
    pl: ['Liczby trafiają do Celery',
        'multiply.delay(a, b) publikuje zadanie z argumentami. Django zwraca identyfikator i HTTP 202.',
        'Samo mnożenie jest szybkie. W tym ćwiczeniu uczymy się przekazywania danych, a nie przyspieszania obliczeń.'
    ],
    en: ['The numbers go to Celery',
        'multiply.delay(a, b) publishes a task with arguments. Django returns an identifier and HTTP 202.',
        'Multiplication is fast. This exercise teaches passing data, not speeding up calculations.'
    ]
}, {
    file: 1,
    context: 'def task_status',
    lines: [],
    needle: 'def task_status',
    span: 8,
    pl: ['Odczytujemy wynik, także zero',
        'Ten sam endpoint statusu odczytuje stan i wynik przez AsyncResult. Po SUCCESS strona wyświetla iloczyn.',
        'Interfejs sprawdza obecność wyniku, nie jego prawdziwość. Dzięki temu 0 nie znika z ekranu.'
    ],
    en: ['Read the result, including zero',
        'The same status endpoint reads state and result with AsyncResult. After SUCCESS, the page displays the product.',
        'The UI checks whether the result exists, not whether it is truthy. This keeps zero visible.'
    ]
}];
questions = [{
    pl: ['Dlaczego pola formularza zamieniamy na liczby?',
        'request.POST zawiera tekst. Bez konwersji nie otrzymalibyśmy prawidłowego mnożenia dwóch liczb.'
    ],
    en: ['Why convert form fields into numbers?',
        'request.POST contains text. Without conversion we would not get correct multiplication of two numbers.'
    ]
}, {
    pl: ['Co przekazuje multiply.delay(6, 7)?',
        'Wiadomość do brokera z nazwą zadania i argumentami 6 oraz 7. Worker odbierze wiadomość i obliczy wynik.'
    ],
    en: ['What does multiply.delay(6, 7) send?',
        'A message containing the task name and arguments 6 and 7. The worker receives it and calculates the result.'
    ]
}, {
    pl: ['Czy wynik 0 oznacza brak wyniku?',
        'Nie. Na przykład 0 × 9 = 0. Obecność wyniku sprawdzamy oddzielnie od jego wartości.'
    ],
    en: ['Does zero mean no result?',
        'No. For example, 0 × 9 = 0. The existence of a result is separate from its value.'
    ]
}, {
    pl: ['Czy warto przenosić każde mnożenie do Celery?',
        'Nie. Dla tak małej operacji komunikacja z brokerem kosztuje więcej niż obliczenie. Celery ma sens przy długotrwałej pracy; tutaj mnożenie służy nauce argumentów i wyników.'
    ],
    en: ['Should every multiplication use Celery?',
        'No. For such a small operation, broker communication costs more than the calculation. Celery makes sense for long-running work; multiplication here teaches arguments and results.'
    ]
}];

function buildMultiplyExamples() {
    const pl = language === 'pl';
    const first = makePage('examples', 0, pl ? 'Pomnóż własne liczby' :
        'Multiply your numbers');
    paragraph(first, pl ?
        'Ten sam mechanizm może przekazywać parametry do generowania raportów lub przetwarzania danych. Tu przekazujemy tylko dwie liczby.' :
        'The same mechanism can pass parameters to report generation or data processing. Here we only pass two numbers.'
        );
    const form = element('form', undefined, 'number-form');
    for (const [name, value] of [
            ['a', '6'],
            ['b', '7']
        ]) {
        const label = element('label', `${pl?'Liczba':'Number'} ${name}`),
            input = element('input');
        input.type = 'number';
        input.name = name;
        input.step = 'any';
        input.required = true;
        input.min = '-1000000000000';
        input.max = '1000000000000';
        input.value = value;
        input.setAttribute('aria-label', `${pl?'Liczba':'Number'} ${name}`);
        label.append(input);
        form.append(label);
    }
    const run = element('button', pl ? 'Oblicz w tle ↗' :
        'Calculate in background ↗', 'primary');
    run.type = 'submit';
    run.dataset.run = '1';
    run.disabled = busy;
    form.append(run);
    form.onsubmit = event => {
        event.preventDefault();
        if (form.reportValidity()) runExamples(1, [{
            a: form.elements.a.value,
            b: form.elements.b.value
        }]);
    };
    first.append(form, makeOutput());
    paragraph(first, pl ?
        'Zakres ćwiczenia: −10¹² do 10¹². Ułamki są dozwolone.' :
        'Exercise range: −10¹² to 10¹². Fractions are allowed.', 'muted');
    stage.append(first);
    const second = makePage('examples', 1, pl ? 'Dodatnie, ujemne i zero' :
        'Positive, negative and zero');
    paragraph(second, pl ?
        'Wyślij trzy niezależne obliczenia: 2 × 3, −4 × 5 oraz 0 × 9. Oczekiwane wyniki to 6, −20 i 0.' :
        'Submit three independent calculations: 2 × 3, −4 × 5 and 0 × 9. Expected results are 6, −20 and 0.'
        );
    paragraph(second, pl ?
        'Każdy zestaw liczb otrzyma własny task_id. Historia zachowa argumenty i wynik każdego zadania.' :
        'Each pair gets its own task_id. The history keeps the arguments and result of each task.',
        'note');
    const runThree = button(pl ? 'Uruchom 3 obliczenia' : 'Run 3 calculations',
        () => runExamples(3, [{
            a: 2,
            b: 3
        }, {
            a: -4,
            b: 5
        }, {
            a: 0,
            b: 9
        }]));
    runThree.dataset.run = '3';
    runThree.disabled = busy;
    second.append(runThree, makeOutput());
    stage.append(second);
    const third = makePage('examples', 2, text('history'));
    paragraph(third, text('historyHint'));
    const history = element('div', undefined, 'course-history');
    history.id = 'execution-history';
    history.setAttribute('aria-live', 'polite');
    third.append(history);
    stage.append(third);
}

