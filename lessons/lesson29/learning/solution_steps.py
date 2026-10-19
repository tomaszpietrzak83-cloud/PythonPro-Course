"""Explanations tied to the exact operation highlighted on each slide."""


def slide(file, needle, pl, en, context=None, also=()):
    item = {"file": file, "needle": needle, "pl": pl, "en": en}
    if context:
        item["context"] = context
    if also:
        item["also"] = list(also)
    return item


DETAILS = {
    3: ("output.write", "Dopisanie wiersza", "Append a line", "write zapisuje znacznik czasu i znak nowej linii do otwartego pliku.", "write appends the timestamp and a newline to the open file.", "Tryb a zachowuje poprzednie wpisy; with zamyka plik.", "Append mode preserves previous entries; with closes the file."),
    4: ("output.write", "Praca po odebraniu zlecenia", "Work after receiving a message", "Worker dopisuje jeden znacznik czasu na każde wykonanie log_timestamp.", "The worker appends one timestamp per log_timestamp execution.", "To worker zapisuje plik. Beat jedynie zleca wykonanie.", "The worker writes the file. Beat only submits the task."),
    5: ('print(f', "Wyjście workera i wynik", "Worker output and result", "print wypisuje liczbę użytkowników; return oddaje tę samą liczbę jako wynik zadania.", "print outputs the user count; return provides the same count as the task result.", "Launcher zapisuje wyjście workera w .runtime/worker.log. Strona odczytuje wynik z backendu.", "The launcher captures worker output in .runtime/worker.log. The page reads the result backend."),
    6: ("count =", "Zliczenie w chwili wykonania", "Count at execution time", "objects.count() wykonuje zapytanie zliczające użytkowników w bazie.", "objects.count() queries the database for the user count.", "Liczba dotyczy chwili wykonania przez workera, nie chwili publikacji zlecenia.", "The count reflects worker execution time, not submission time."),
    7: ("user.last_login =", "Aktualizacja jednego pola", "Update one field", "Ustawiamy bieżący czas, a save(update_fields=...) zapisuje tylko last_login.", "We set the current time; save(update_fields=...) persists only last_login.", "To ćwiczenie zmiany pola; nie loguje użytkownika do aplikacji.", "This field-update exercise does not log a user into the app."),
    8: ("time.sleep(15)", "Symulowane oczekiwanie", "Simulated waiting", "sleep zajmuje proces workera przez 15 sekund. Dopiero potem funkcja zwraca komunikat zakończenia.", "sleep occupies the worker for fifteen seconds. The function then returns its completion message.", "Odpowiedź Django nie czeka na ten sleep; inne zadania w tej samej kolejce mogą czekać.", "Django does not wait for this sleep; other tasks in this queue may wait."),
    9: ("return a * b", "Wynik pojedynczego zlecenia", "One submission's result", "Każde wykonanie multiply oblicza iloczyn własnej pary argumentów.", "Each multiply execution computes the product of its own argument pair.", "Pięćdziesiąt zleceń ma pięćdziesiąt osobnych wyników.", "Fifty submissions have fifty separate results."),
    10: ("notification.sent_at =", "Zapis czasu symulowanej wysyłki", "Record simulated delivery time", "Po sleep(2) ustawiamy sent_at i zapisujemy to pole w bazie.", "After sleep(2), we set sent_at and persist that field in the database.", "Ten kod nie wysyła prawdziwego maila.", "This code does not send real email."),
    11: ("self.update_state", "Publikacja metadanych", "Publish metadata", "update_state zapisuje własny stan PROGRESS oraz current i total w backendzie wyników.", "update_state stores custom PROGRESS state and current/total in the result backend.", "PROGRESS 100 nie jest jeszcze SUCCESS; funkcja musi zakończyć się poprawnie.", "PROGRESS 100 is not yet SUCCESS; the function must finish successfully."),
    12: ("deleted, _ =", "Usunięcie starych logów", "Delete old logs", "filter(created_at__lt=cutoff) wybiera rekordy ściśle starsze od granicy; delete je usuwa.", "filter(created_at__lt=cutoff) selects rows strictly older than the cutoff; delete removes them.", "Rekord równy granicy pozostaje. deleted to liczba usuniętych obiektów zwrócona przez Django.", "A row exactly at the cutoff remains. deleted is Django's deleted-object count."),
    14: ("for user in get_user_model", "Wiersze raportu", "Report rows", "iterator odczytuje użytkowników partiami. writer.writerow zapisuje username i email każdego z nich.", "iterator reads users in batches. writer.writerow writes each username and email.", "Prefiks apostrofu chroni pola zaczynające się od =, +, - lub @ przed interpretacją jako formuły arkusza.", "An apostrophe prefix protects fields starting with =, +, - or @ from spreadsheet formula interpretation."),
    15: ("raise self.retry", "Ponowienie po błędzie", "Retry after an error", "Po RequestException self.retry zleca ponowną próbę z countdown=60 i przerywa obecną.", "After RequestException, self.retry schedules another attempt with countdown=60 and ends the current one.", "Ponowienia zachowują task_id. Pierwsza próba plus maksymalnie trzy ponowienia. 60 sekund to opóźnienie zlecenia, nie gwarancja dokładnej chwili wykonania.", "Retries keep the same task_id. One initial attempt plus at most three retries. Sixty seconds is the scheduling delay, not an exact execution-time guarantee."),
    16: ("gray =", "Porównanie kanałów RGB", "Compare RGB channels", "difference i getbbox sprawdzają, czy R=G oraz G=B dla wszystkich pikseli. Brak różnic oznacza skalę szarości.", "difference and getbbox check whether R=G and G=B for every pixel. No differences means grayscale.", "Sprawdzamy piksele po konwersji do RGB; sam format pliku nie określa klasyfikacji.", "We inspect pixels after RGB conversion; the file format alone does not determine classification."),
    18: ("notification.sent_at =", "Ta sama funkcja mailowa", "The same email function", "Worker kolejki priority_queue symuluje wysyłkę, ustawia sent_at i zapisuje pole.", "The priority_queue worker simulates delivery, sets sent_at and saves the field.", "Funkcja jest wspólna z zadaniem 10. Wybór kolejki odbywa się poza jej treścią.", "The function is shared with task 10. Queue selection happens outside its body."),
    19: ("print(message", "Wykonanie nadal w workerze", "Execution still happens in a worker", "hello_world wypisuje komunikat i zwraca go jako wynik, tak samo jak w zadaniu 1.", "hello_world outputs a message and returns it, just as in task 1.", "Flower jest monitorem i producentem zleceń; nie wykonuje tej funkcji.", "Flower monitors and submits tasks; it does not execute this function."),
    20: ("record.save", "Zapis wyniku przetwarzania", "Persist processing results", "Worker zapisuje text zamieniony na wielkie litery oraz processed_at.", "The worker saves uppercased text and processed_at.", "Ten zapis jest osobną operacją po zatwierdzeniu transakcji tworzącej rekord.", "This write is a separate operation after the record-creation transaction commits."),
}


def get_solution_steps(number, anchor, operation_pl, operation_en):
    steps = [slide(0, anchor,
        ["Funkcja workera", operation_pl, "@shared_task rejestruje funkcję; sam dekorator jej nie uruchamia."],
        ["Worker function", operation_en, "@shared_task registers the function; the decorator itself does not run it."], anchor)]
    if number in DETAILS:
        needle, title_pl, title_en, body_pl, body_en, note_pl, note_en = DETAILS[number]
        also = {5: ["return count"], 7: ["user.save"], 8: ["return"],
                10: ["notification.save"], 18: ["notification.save"],
                19: ["return message"]}.get(number, [])
        steps.append(slide(0, needle, [title_pl, body_pl, note_pl],
                           [title_en, body_en, note_en], anchor, also))
    if number == 13:
        steps = [slide(0, "response = requests.get",
            ["Pobranie HTML", "requests.get pobiera https://example.com. raise_for_status zgłasza błąd dla odpowiedzi HTTP 4xx i 5xx.", "timeout=15 ogranicza czekanie na połączenie i bezczynność odczytu; nie jest limitem 15 sekund dla całego zadania."],
            ["Fetch HTML", "requests.get fetches https://example.com. raise_for_status raises for HTTP 4xx and 5xx responses.", "timeout=15 limits connection waiting and read inactivity; it is not a fifteen-second deadline for the entire task."], anchor, ["response.raise_for_status"]),
            slide(0, "title = BeautifulSoup",
            ["Odczyt tytułu", "BeautifulSoup analizuje response.text. title wybiera element <title>, a get_text(strip=True) pobiera tekst bez otaczających odstępów.", "Parser nie wykonuje JavaScript. Ten przykład zakłada obecność elementu <title>; jego brak spowodowałby błąd."],
            ["Read the title", "BeautifulSoup parses response.text. title selects <title>; get_text(strip=True) extracts text without surrounding whitespace.", "The parser does not execute JavaScript. This example assumes a <title> element; its absence would cause an error."], anchor),
            slide(0, "page = ScrapedPage.objects.create",
            ["Zapis do bazy i wynik", "objects.create tworzy nowy ScrapedPage z URL i tytułem. return oddaje ID, tytuł i URL do backendu wyników.", "Każde poprawne wykonanie dodaje nowy rekord. Wynik Celery i rekord Django to osobne miejsca przechowywania."],
            ["Database write and result", "objects.create inserts a new ScrapedPage with its URL and title. return supplies its ID, title and URL to the result backend.", "Each successful execution adds a new row. The Celery result and Django row are separate storage locations."], anchor, ['return {"id": page.pk'])]
    if number == 17:
        steps = [slide(0, "def random_number",
            ["Pierwszy krok: losowanie", "random.randint(1, 100) zwraca liczbę całkowitą, uwzględniając obie granice.", "Ta liczba stanie się argumentem drugiego kroku."],
            ["First step: random number", "random.randint(1, 100) returns an integer, including both endpoints.", "This number becomes the second step's argument."]),
            slide(0, "def times_ten",
            ["Drugi krok: mnożenie", "times_ten przyjmuje wynik losowania i zwraca number * 10.", "Nie losuje ponownie; przetwarza wynik poprzedniego kroku."],
            ["Second step: multiplication", "times_ten receives the generated number and returns number * 10.", "It does not generate another number; it transforms the previous result."]),
            slide(0, "def save_number",
            ["Trzeci krok: plik", "save_number zapisuje otrzymaną liczbę w media, używając ID tego kroku w nazwie pliku. Zwraca liczbę i link.", "bind=True udostępnia self.request.id. Każde wykonanie zapisuje osobny plik."],
            ["Third step: file", "save_number writes the received number under media, using this step's ID in the filename. It returns the number and a link.", "bind=True provides self.request.id. Each execution writes a separate file."])]
    if number in (14, 16):
        steps.append(slide(0, 'return {"filename": filename' if number == 14 else "record.classification_result =",
            ["Udostępnienie wyniku", "return zwraca nazwę i URL po wyjściu z with, czyli po zamknięciu CSV." if number == 14 else "Przypisujemy opis klasyfikacji do modelu i zapisujemy go przez save. return udostępnia ID, opis i URL obrazu.", "Plik lub rekord w bazie jest osobnym efektem wykonania. Backend Celery przechowuje zwrócony słownik."],
            ["Expose the result", "return supplies the filename and URL after leaving with, so after the CSV file is closed." if number == 14 else "We assign the classification description to the row and persist it with save. return supplies the ID, description and image URL.", "The file or database row is a separate execution effect. Celery's backend stores the returned dictionary."], anchor,
            ["record.save", 'return {"id": record.pk'] if number == 16 else []))
    schedules = {
        4: ('"timestamp-every-ten-seconds"', "Co 10 sekund", "Every ten seconds", "schedule=10.0 określa odstęp publikowania log_timestamp. Zajęty worker może wykonać zadanie później.", "schedule=10.0 defines the log_timestamp submission interval. A busy worker may execute it later."),
        6: ('"users-at-23"', "Codziennie o 23:00", "Daily at 23:00", "crontab(hour=23, minute=0) zleca count_users o 23:00 w Europe/Warsaw.", "crontab(hour=23, minute=0) schedules count_users at 23:00 in Europe/Warsaw."),
        12: ('"daily-log-cleanup"', "Codzienna retencja", "Daily cleanup", "crontab(hour=0, minute=15) zleca clean_logs codziennie o 00:15 w Europe/Warsaw.", "crontab(hour=0, minute=15) schedules clean_logs daily at 00:15 in Europe/Warsaw."),
        13: ('"hourly-page-title"', "O pełnej godzinie", "At the top of each hour", "crontab(minute=0) zleca scrape_title o każdej pełnej godzinie w Europe/Warsaw, np. 10:00 i 11:00.", "crontab(minute=0) schedules scrape_title at each full hour in Europe/Warsaw, such as 10:00 and 11:00."),
    }
    if number in schedules:
        needle, pl, en, body_pl, body_en = schedules[number]
        steps.append(slide(4, needle,
            [pl, body_pl, "To reguła publikowania. Wykonanie wymaga działającego Beat, brokera i workera."],
            [en, body_en, "This is a submission rule. Execution requires running Beat, a broker and a worker."]))
        steps.append(slide(7, "beat = logged_process",
            ["Uruchomienie Beat", "Launcher uruchamia osobny proces celery beat z aplikacją academy i plikiem stanu harmonogramu.", "Beat czyta ustawienia i publikuje zadania. Nie wykonuje funkcji workera; potrzebna jest jedna instancja tego harmonogramu."],
            ["Start Beat", "The launcher starts a separate celery beat process with the academy app and a schedule-state file.", "Beat reads settings and publishes tasks. It does not execute worker functions; run one instance of this scheduler."], "def main"))
    if number == 9:
        steps.append(slide(6, "def handle",
            ["Komenda tworzy 50 zleceń", "Pętla range(50) losuje dwie liczby od -20 do 20, publikuje multiply.delay(a, b) i zbiera ID oraz argumenty.", "stdout.write wypisuje listę jako JSON. Komenda nie czeka na wyniki; worker solo wykonuje zadania kolejno."],
            ["Command creates fifty submissions", "range(50) generates two integers from -20 to 20, publishes multiply.delay(a, b), and collects IDs and arguments.", "stdout.write emits the list as JSON. The command does not wait for results; a solo worker handles tasks sequentially."]))
    if number in (10, 16):
        name = "EmailNotification" if number == 10 else "UploadedImage"
        steps.append(slide(5, "class " + name,
            ["Model danych", "EmailNotification przechowuje adres, temat, treść i nullable sent_at." if number == 10 else "ImageField przechowuje nazwę zapisanego pliku; classification_result jest początkowo pustym tekstem.", "Rekord powstaje przed zleceniem pracy. Worker otrzymuje jego ID."],
            ["Data model", "EmailNotification stores recipient, subject, body and nullable sent_at." if number == 10 else "ImageField stores the saved file's name; classification_result starts as empty text.", "The row is created before submission. The worker receives its ID."]))
    if number == 18:
        steps.extend([slide(4, "CELERY_TASK_ROUTES",
            ["Wybór kolejki", "Pełna nazwa learning.tasks.send_notification wskazuje priority_queue. Pozostałe zadania używają skonfigurowanej kolejki default.", "Nazwa priority_queue nie ustawia priorytetu wiadomości. Izolację zapewni osobny worker."],
            ["Select a queue", "The full name learning.tasks.send_notification selects priority_queue. Other tasks use the configured default queue.", "The name priority_queue does not assign message priority. A separate worker provides isolation."], also=["CELERY_TASK_DEFAULT_QUEUE"]),
            slide(7, "priority = logged_process",
            ["Worker dla priority_queue", "Launcher uruchamia osobnego workera z -Q priority_queue i własną nazwą. Ten proces odbiera zadania mailowe.", "Domyślny worker słucha default, więc symulacja filmu nie zajmuje workera mailowego."],
            ["Worker for priority_queue", "The launcher starts a separately named worker with -Q priority_queue. This process receives email tasks.", "The default worker listens to default, so video simulation does not occupy the email worker."], "def main")])
    if number == 19:
        steps.append(slide(7, "flower = logged_process",
            ["Uruchomienie Flower", "Launcher uruchamia Flower dla academy na lokalnym porcie 5559. Flower korzysta z tego samego brokera co workery.", "Dashboard zbiera zdarzenia workera. Lokalna demonstracja udostępnia też API do zlecania zadań."],
            ["Start Flower", "The launcher starts Flower for academy on local port 5559. Flower uses the same broker as the workers.", "The dashboard collects worker events. The local demonstration also enables its task-submission API."], "def main"))
    if number == 20:
        steps.extend([slide(1, "with transaction.atomic",
            ["Transakcja tworząca rekord", "atomic obejmuje utworzenie ProcessingRecord i rejestrację callbacku. Opcja rollback zgłasza wyjątek przed zatwierdzeniem.", "Przy rollback znika nowy rekord i callback; odpowiedź ROLLED_BACK nie zawiera task_id, bo niczego nie zlecono."],
            ["Record-creation transaction", "atomic encloses ProcessingRecord creation and callback registration. The rollback option raises before commit.", "Rollback discards the new row and callback. ROLLED_BACK has no task_id because no task was submitted."], "def create_transaction_record"),
            slide(1, "transaction.on_commit",
            ["Zlecenie dopiero po COMMIT", "Callback wywoła apply_async po zatwierdzeniu, przekazując ID rekordu i wcześniej przygotowane task_id.", "Zatwierdzenie bazy i publikacja do brokera nie są jedną atomową operacją: awaria publikacji może pozostawić zapisany rekord."],
            ["Submit only after COMMIT", "After commit, the callback invokes apply_async with the row ID and the preallocated task_id.", "Database commit and broker publication are not one atomic operation: failed publication may leave the saved row."], "def create_transaction_record")])
    dispatch = {3: "if task_number in (3, 4)", 4: "if task_number in (3, 4)",
                5: "elif task_number in (5, 6)", 6: "elif task_number in (5, 6)",
                10: "elif task_number in (10, 18)", 18: "elif task_number in (10, 18)"}
    view_notes = {
        7: ("Widok sprawdza ID i istnienie użytkownika, następnie przekazuje samo ID do update_user_last_login.delay.", "The view validates the ID and user existence, then passes only the ID to update_user_last_login.delay."),
        8: ("Widok zleca process_video.delay bez czekania na sleep. W odpowiedzi 202 dodaje komunikat rozpoczęcia.", "The view submits process_video.delay without waiting for sleep. Its 202 response adds the started message."),
        9: ("Widok uruchamia enqueue_tasks przez call_command i odczytuje JSON z jego stdout. Odpowiedź zawiera listę 50 zleceń i task_id pierwszego.", "The view invokes enqueue_tasks through call_command and reads its stdout JSON. The response contains fifty submissions and the first task's ID."),
        10: ("Po walidacji adresu widok tworzy powiadomienie, a następnie przekazuje jego ID do send_notification.delay.", "After validating the email address, the view creates a notification and passes its ID to send_notification.delay."),
        16: ("Widok sprawdza obecność i rozmiar pliku (maks. 5 MB), weryfikuje obraz, cofa wskaźnik pliku, zapisuje model i zleca klasyfikację po ID.", "The view checks for a file and its size (max 5 MB), verifies the image, rewinds the file, saves the row and submits classification by ID."),
        17: ("chain łączy trzy sygnatury .s(). Wywołanie łańcucha publikuje pierwszy krok; kolejne otrzymają wynik poprzednika.", "chain combines three .s() signatures. Calling the chain publishes the first step; subsequent steps receive their predecessor's result."),
        18: ("Widok tworzy powiadomienie i wywołuje send_notification.delay. Routing z settings wybiera priority_queue bez argumentu queue w widoku.", "The view creates a notification and calls send_notification.delay. Settings routing selects priority_queue without a queue argument in the view."),
        19: ("Widok wysyła POST do API Flower, sprawdza odpowiedź HTTP i odczytuje task-id. Flower publikuje hello_world do brokera.", "The view posts to Flower's API, checks the HTTP response and reads task-id. Flower publishes hello_world to the broker."),
    }
    if number != 20:
        body_pl, body_en = view_notes.get(number, (
            "Widok wywołuje .delay() wskazanego zadania. Po publikacji zwraca task_id i odpowiedź HTTP 202.",
            "The view calls .delay() for the highlighted task. After publication it returns task_id and HTTP 202."))
        notes = ("task_id dotyczy ostatniego kroku, save_number. Nie identyfikuje całego łańcucha jako jednego wykonania." if number == 17 else
                 "Komenda czeka na publikację wszystkich zleceń, lecz nie na ich wykonanie. Wyniki są osobne dla każdego ID." if number == 9 else
                 "202 potwierdza zlecenie, a nie rozpoczęcie lub zakończenie pracy workera.")
        notes_en = ("task_id identifies the final save_number step, not the entire chain as one execution." if number == 17 else
                    "The command waits to publish all submissions, but not for execution. Each ID has its own result." if number == 9 else
                    "202 confirms submission, not that worker execution has started or finished.")
        also = ['if task_number == 8:', 'return JsonResponse(payload'] if number == 8 else []
        steps.append(slide(1, dispatch.get(number, f"elif task_number == {number}:"),
            ["Zlecenie z widoku", body_pl, notes], ["Submission from the view", body_en, notes_en],
            "def run_exercise", also))
    steps.append(slide(1, "def task_status",
        ["Odczyt stanu i wyniku", "AsyncResult odczytuje stan po task_id. Endpoint zwraca wynik po SUCCESS, ogólny błąd po FAILURE i metadane po PROGRESS.", "PENDING może też oznaczać nieznane ID. RETRY nie jest końcem zadania; ten endpoint nie zwraca szczegółów wyjątku."],
        ["Read state and result", "AsyncResult reads state by task_id. The endpoint returns a result for SUCCESS, a generic error for FAILURE and metadata for PROGRESS.", "PENDING can also mean an unknown ID. RETRY is not completion; this endpoint does not return exception details."], "def task_status"))
    return steps
