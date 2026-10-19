"""Bilingual, task-specific teaching material; code slides reference live files."""

import re
from pathlib import Path

# number: English assignment, PL concept, EN concept, PL pitfall, EN pitfall,
# main code anchor, optional second anchor, sample
LESSONS = {
    3: (
        "Write log_timestamp() to append the current date and time to log.txt.",
        "Efekt uboczny",
        "Side effects",
        "return zwraca wynik, a zapis do pliku zmienia stan dysku. Ponowne wywołanie dopisze kolejny wiersz.",
        "return produces a result; writing a file changes disk state. Repeating the task appends another line.",
        "def log_timestamp",
        "output.write",
        "log_timestamp() → log.txt",
    ),
    4: (
        "Use Celery Beat to run log_timestamp() every 10 seconds.",
        "Beat jest zegarem",
        "Beat is the clock",
        "Beat publikuje wiadomości, ale ich nie wykonuje. Potrzebujesz także brokera i workera. Uruchamiaj tylko jedną instancję Beat.",
        "Beat publishes messages but does not execute them. A broker and worker are also needed. Run only one Beat instance.",
        "def log_timestamp",
        "output.write",
        "10 s → Beat → worker → log.txt",
    ),
    5: (
        "Count all users using User.objects.count() and print the count in the worker console.",
        "ORM w workerze",
        "The ORM inside a worker",
        "count() pyta bazę o liczbę rekordów, bez pobierania wszystkich obiektów do pamięci. Dane odczytujemy w chwili wykonania.",
        "count() asks the database for a count without loading every object. Data is read when the task executes.",
        "def count_users",
        "print(f",
        "User.objects.count()",
    ),
    6: (
        "Schedule count_users() every day at 23:00 with Celery Beat and crontab.",
        "Godzina a odstęp",
        "Clock time versus interval",
        "crontab(hour=23, minute=0) oznacza konkretną godzinę w strefie Europe/Warsaw. Odstęp 24 h nie wyraża tego samego harmonogramu.",
        "crontab(hour=23, minute=0) specifies a clock time in Europe/Warsaw. A 24-hour interval does not express the same schedule.",
        "def count_users",
        "get_user_model().objects.count",
        "crontab(hour=23, minute=0)",
    ),
    7: (
        "Accept user_id, load the user from the database and set last_login to the current time.",
        "Przekazuj ID",
        "Pass an ID",
        "Przesyłamy liczbę, a nie obiekt Django. Worker pobiera aktualny rekord. To ćwiczenie aktualizacji pola, a nie rzeczywisty proces uwierzytelnienia.",
        "Send a number rather than a Django object. The worker loads the current record. This is a field-update exercise, not a real authentication flow.",
        "def update_user_last_login",
        "user.save",
        "update_user_last_login(user_id)",
    ),
    8: (
        "Simulate video processing with time.sleep(15); immediately respond that processing has started.",
        "Odpowiedź bez czekania",
        "Respond without waiting",
        "sleep(15) blokuje workera przez 15 sekund, ale nie widok Django. To symulacja, nie dekodowanie filmu.",
        "sleep(15) blocks the worker for 15 seconds, but not the Django view. This is a simulation, not video decoding.",
        "def process_video",
        "time.sleep(15)",
        "HTTP 202 teraz → wynik za około 15 s",
    ),
    9: (
        "Create an enqueue_tasks management command that submits 50 multiply tasks with random arguments.",
        "Producent masowy",
        "A batch producer",
        "50 wiadomości oznacza 50 niezależnych task_id. Nasz worker solo wykonuje je kolejno; nie powstaje 50 procesów.",
        "50 messages mean 50 independent task IDs. Our solo worker handles them sequentially; this does not create 50 processes.",
        "def multiply",
        "return a * b",
        "python manage.py enqueue_tasks",
    ),
    10: (
        "Create EmailNotification with recipient_email, subject, body and nullable sent_at; simulate delivery and update sent_at.",
        "Stan w bazie",
        "Persisted state",
        "NULL w sent_at oznacza brak potwierdzonej wysyłki. W ćwiczeniu jedynie symulujemy mail; ponawianie rzeczywistej wysyłki wymaga ochrony przed duplikatami.",
        "NULL in sent_at means no confirmed delivery. Email is simulated here; retrying actual delivery requires duplicate protection.",
        "def send_notification",
        "notification.save",
        "ID → opóźnienie → sent_at",
    ),
    11: (
        "Loop from 1 to 100, sleep 0.1 seconds and publish PROGRESS metadata. Provide /task-status/<task_id>/.",
        "Stan i metadane",
        "State and metadata",
        "bind=True udostępnia self. PROGRESS jest własnym stanem, a current i total to metadane. Stan SUCCESS potwierdza dopiero zakończenie.",
        "bind=True provides self. PROGRESS is a custom state; current and total are metadata. Only SUCCESS confirms completion.",
        "def track_progress",
        "self.update_state",
        "PROGRESS {current: 42, total: 100}",
    ),
    12: (
        "Create LogEntry, delete entries older than 90 days and schedule cleanup daily.",
        "Granica retencji",
        "Retention boundary",
        "created_at__lt usuwa rekordy ściśle starsze od granicy. To rzeczywiste usunięcie danych demonstracyjnych; kolejne wywołanie może usunąć zero rekordów.",
        "created_at__lt removes rows strictly older than the cutoff. Demo records are really deleted; another run may delete zero rows.",
        "def clean_logs",
        "created_at__lt",
        "teraz − 90 dni → DELETE",
    ),
    13: (
        "Fetch https://example.com using requests and BeautifulSoup, store the title in the database and schedule it hourly.",
        "Sieć w tle",
        "Network work in the background",
        "timeout ogranicza czekanie na połączenie i bezczynność odczytu, a nie łączny czas zadania. raise_for_status odrzuca błędne odpowiedzi HTTP. BeautifulSoup odczytuje HTML, nie uruchamia JavaScript.",
        "timeout limits connection waiting and read inactivity, not total task duration. raise_for_status rejects unsuccessful HTTP responses. BeautifulSoup reads HTML; it does not execute JavaScript.",
        "def scrape_title",
        "ScrapedPage.objects.create",
        "HTML → <title> → baza",
    ),
    14: (
        "Generate a CSV containing all usernames and emails in media; return task_id and expose a download link when finished.",
        "Zlecenie i artefakt",
        "Submission and artifact",
        "Nie zwracamy całego CSV przez backend wyników. Zwracamy nazwę i link dopiero po zamknięciu pliku. Każde wywołanie ma osobny plik.",
        "The result backend does not carry the entire CSV. It returns a filename and link after the file is closed. Each execution gets its own file.",
        "def generate_csv",
        "writer.writerow",
        "task_id → SUCCESS → pobierz CSV",
    ),
    15: (
        "Connect to a nonexistent URL and retry three times, one minute apart, using self.retry.",
        "Ponowienie z tym samym ID",
        "Retry keeps the same ID",
        "Pierwsza próba + trzy ponowienia = cztery próby. RETRY nie oznacza zakończenia. Po około trzech minutach oczekujemy FAILURE, bo adres celowo nie istnieje.",
        "The first attempt plus three retries means four attempts. RETRY is not completion. After about three minutes FAILURE is expected because the address deliberately does not exist.",
        "def retry_connection",
        "self.retry",
        "countdown=60, max_retries=3",
    ),
    16: (
        "Save an uploaded image, pass its ID to Celery, classify grayscale/color and dimensions using Pillow, and persist the result.",
        "Prosta klasyfikacja",
        "Simple classification",
        "Porównujemy kanały RGB pikseli, więc również szary obraz zapisany jako RGB będzie rozpoznany. To reguła, a nie wytrenowany model AI.",
        "We compare pixel RGB channels, so a gray image stored as RGB is also recognized. This is a rule, not a trained AI model.",
        "def classify_image",
        "ImageChops.difference",
        "plik → ID → Pillow → wynik w bazie",
    ),
    17: (
        "Chain three tasks: generate a random number, multiply it by ten, save it to a file; invoke the chain from a Django view.",
        "Wynik jest argumentem",
        "A result becomes an argument",
        ".s() tworzy sygnaturę. chain przekazuje wynik poprzedniego zadania do następnego. Zwrócone task_id identyfikuje ostatni krok.",
        ".s() creates a signature. chain passes the previous task result into the next task. The returned task ID identifies the final step.",
        "def random_number",
        "def save_number",
        "random_number.s() → times_ten.s() → save_number.s()",
    ),
    18: (
        "Configure default and priority_queue, route email tasks to priority_queue, and start one worker for each queue.",
        "Izolacja kolejek",
        "Queue isolation",
        "Osobny worker może obsłużyć mail, gdy domyślny przetwarza film. Nazwa priority_queue sama nie nadaje priorytetu wiadomościom; izolację zapewnia drugi worker.",
        "A separate worker can handle email while the default worker processes video. The name priority_queue alone does not prioritize messages; the second worker provides isolation.",
        "def send_notification",
        "notification.sent_at",
        "default → worker A | priority_queue → worker B",
    ),
    19: (
        "Install Flower, inspect dashboard, tasks and workers, and submit a task using Flower's interface/API.",
        "Obserwacja procesów",
        "Observe processes",
        "Flower słucha zdarzeń Celery. Otwórz Dashboard, Tasks i stronę wybranego workera. Przycisk w tym przykładzie zleca zadanie przez rzeczywiste API Flower.",
        "Flower listens to Celery events. Open Dashboard, Tasks and an individual worker page. This example button submits a task through the actual Flower API.",
        "def hello_world",
        "print(message",
        "Flower: http://127.0.0.1:5559",
    ),
    20: (
        "Create a database object inside transaction.atomic and process it with Celery only after the transaction commits.",
        "Zatwierdź, potem zleć",
        "Commit, then publish",
        "Worker przed COMMIT może nie widzieć rekordu. on_commit uruchamia zlecenie dopiero po zatwierdzeniu. Przy rollback callback znika. Nie gwarantuje to atomowości bazy i brokera.",
        "Before COMMIT the worker may not see the record. on_commit publishes after a successful commit. Rollback discards the callback. This does not make database and broker atomic together.",
        "def process_record",
        "record.save",
        "atomic → INSERT → COMMIT → on_commit → Celery",
    ),
}

TASK_QUESTIONS = {
    3: [
        (
            "Dlaczego tryb 'a', a nie 'w'?",
            "'a' dopisuje kolejne wiersze. 'w' kasowałby poprzednią zawartość przy każdym uruchomieniu.",
            "Why 'a' rather than 'w'?",
            "'a' appends lines. 'w' would replace previous contents on each execution.",
        ),
        (
            "Gdzie powstaje log.txt?",
            "W katalogu lesson29, niezależnie od katalogu, z którego uruchomisz worker. Ścieżkę wyznacza settings.BASE_DIR.",
            "Where is log.txt created?",
            "In lesson29, regardless of the worker's starting directory. settings.BASE_DIR determines the path.",
        ),
    ],
    4: [
        (
            "Czy Beat wykona funkcję bez workera?",
            "Nie. Beat zleca pracę, a worker ją wykonuje. Wiadomości mogą czekać w kolejce.",
            "Will Beat execute without a worker?",
            "No. Beat submits work and a worker executes it. Messages may wait in the queue.",
        ),
        (
            "Czy wynik pojawi się dokładnie co 10 sekund?",
            "To odstęp publikowania zleceń. Zajęty worker może zapisać wynik później.",
            "Will results appear exactly every ten seconds?",
            "That is the submission interval. A busy worker may write the result later.",
        ),
    ],
    5: [
        (
            "Czy trzeba pobrać listę wszystkich użytkowników?",
            "Nie. count() wykonuje zapytanie zliczające w bazie i zwraca liczbę.",
            "Must we load every user?",
            "No. count() performs a database count query and returns a number.",
        ),
        (
            "Dlaczego konsola i przeglądarka widzą wynik?",
            "print() zapisuje go w logu workera; return przechowuje go w backendzie wyników.",
            "Why can both console and browser show the count?",
            "print() writes to the worker log; return stores it in the result backend.",
        ),
    ],
    6: [
        (
            "W jakiej strefie działa godzina 23:00?",
            "W Europe/Warsaw, ustawionej przez CELERY_TIMEZONE. To ważne przy zmianie czasu.",
            "Which timezone defines 23:00?",
            "Europe/Warsaw, configured by CELERY_TIMEZONE. This matters for daylight saving time.",
        ),
        (
            "Czy przycisk zmienia harmonogram?",
            "Nie. Zleca dodatkowe wykonanie count_users teraz. Codzienny harmonogram pozostaje aktywny.",
            "Does the button change the schedule?",
            "No. It submits an extra count_users execution now. The daily schedule remains active.",
        ),
    ],
    7: [
        (
            "Dlaczego przekazujemy user_id?",
            "ID da się przesłać jako JSON. Worker pobiera aktualny obiekt, zamiast otrzymywać przestarzały stan modelu.",
            "Why pass user_id?",
            "An ID can be serialized as JSON. The worker loads the current object instead of receiving stale model state.",
        ),
        (
            "Co jeśli użytkownik zostanie usunięty po zleceniu?",
            "Walidacja widoku tego nie wyklucza. Odczyt w workerze rzuci DoesNotExist, więc zadanie zakończy się FAILURE.",
            "What if the user is deleted after submission?",
            "View validation cannot prevent that race. The worker raises DoesNotExist and the task fails.",
        ),
    ],
    8: [
        (
            "Czy sleep(15) blokuje Django?",
            "Nie, ponieważ działa w osobnym procesie. Zajmuje jednak domyślnego workera.",
            "Does sleep(15) block Django?",
            "No, it runs in another process. It does occupy the default worker.",
        ),
        (
            "Co potwierdza komunikat rozpoczęcia?",
            "Przyjęcie zlecenia. Przy zajętym workerze przetwarzanie może jeszcze czekać w kolejce.",
            "What does the started message confirm?",
            "Acceptance of the submission. With a busy worker, processing may still be queued.",
        ),
    ],
    9: [
        (
            "Czy 50 zadań ma jeden task_id?",
            "Nie. Każda wiadomość ma własny identyfikator oraz własne argumenty i wynik.",
            "Do fifty tasks share one ID?",
            "No. Each message has its own ID, arguments and result.",
        ),
        (
            "Gdzie uruchomić komendę?",
            "W lesson29: python manage.py enqueue_tasks. Ustaw ten sam broker co worker, np. LESSON29_BROKER_URL dla Redisa.",
            "Where do you run the command?",
            "In lesson29: python manage.py enqueue_tasks. Configure the same broker as the worker, such as LESSON29_BROKER_URL for Redis.",
        ),
    ],
    10: [
        (
            "Po co nullable sent_at?",
            "Obiekt istnieje przed zakończeniem pracy. NULL odróżnia oczekiwanie od zapisanej daty symulowanej wysyłki.",
            "Why is sent_at nullable?",
            "The object exists before completion. NULL distinguishes pending delivery from a recorded simulated send time.",
        ),
        (
            "Czy wysłaliśmy prawdziwy mail?",
            "Nie. Zgodnie z zadaniem sleep symuluje opóźnienie, a sent_at jest aktualizowane w bazie.",
            "Did we send real email?",
            "No. As required, sleep simulates delay and sent_at is updated in the database.",
        ),
    ],
    11: [
        (
            "Po co bind=True?",
            "Przekazuje instancję zadania jako self, dzięki czemu możemy wywołać update_state().",
            "Why bind=True?",
            "It passes the task instance as self so we can call update_state().",
        ),
        (
            "Czy PROGRESS 100 oznacza już SUCCESS?",
            "Nie. Pętla opublikowała postęp, ale funkcja musi jeszcze poprawnie zakończyć wykonanie.",
            "Is PROGRESS 100 already SUCCESS?",
            "No. The loop reported progress, but the function must still finish successfully.",
        ),
    ],
    12: [
        (
            "Które rekordy usuwa __lt?",
            "Ściśle starsze od granicy teraz minus 90 dni. Rekord równy granicy nie spełnia __lt.",
            "Which records does __lt remove?",
            "Records strictly older than now minus ninety days. A record equal to the cutoff does not match __lt.",
        ),
        (
            "Dlaczego drugie wykonanie usuwa zero?",
            "Pierwsze już usunęło stare rekordy. Powtórzenie jest bezpieczne, dopóki nowe rekordy nie przekroczą granicy retencji.",
            "Why might the second run delete zero?",
            "The first run already removed old records. Repetition is safe until other rows cross the retention boundary.",
        ),
    ],
    13: [
        (
            "Po co timeout i raise_for_status?",
            "timeout ogranicza czekanie na połączenie i bezczynność odczytu; raise_for_status wykrywa HTTP 4xx/5xx. Bez nich worker mógłby czekać długo lub analizować stronę błędu.",
            "Why timeout and raise_for_status?",
            "timeout limits connection waiting and read inactivity; raise_for_status detects HTTP 4xx/5xx. Otherwise a worker could wait too long or parse an error page.",
        ),
        (
            "Czy BeautifulSoup zobaczy treść utworzoną przez JavaScript?",
            "Nie wykonuje JavaScript. W tym zadaniu tytuł jest już w pobranym HTML.",
            "Does BeautifulSoup see JavaScript-generated content?",
            "It does not execute JavaScript. This exercise's title is already in the downloaded HTML.",
        ),
    ],
    14: [
        (
            "Dlaczego nazwa pliku zawiera task_id?",
            "Kolejne raporty nie nadpisują się nawzajem. Wynik każdego zlecenia wskazuje własny plik.",
            "Why does the filename contain task_id?",
            "Separate reports do not overwrite one another. Each execution points to its own file.",
        ),
        (
            "Kiedy pokazujemy link?",
            "Po SUCCESS, gdy zapis i zamknięcie pliku zostały zakończone. Wcześniej samo task_id nie potwierdza gotowego raportu.",
            "When do we expose the link?",
            "After SUCCESS, when writing and closing the file are complete. A task ID alone does not mean a report is ready.",
        ),
    ],
    15: [
        (
            "Ile jest łącznie prób?",
            "Cztery: pierwsza plus trzy ponowienia. Odstęp countdown wynosi 60 sekund.",
            "How many attempts are made?",
            "Four: the initial attempt plus three retries. countdown is sixty seconds.",
        ),
        (
            "Dlaczego końcowy FAILURE jest poprawny?",
            "Adres .invalid celowo nie istnieje. Ćwiczymy wyczerpanie limitu ponowień, a nie udane pobranie strony.",
            "Why is final FAILURE correct?",
            "The .invalid address deliberately does not exist. We are demonstrating exhausted retries, not a successful fetch.",
        ),
    ],
    16: [
        (
            "Czy obraz RGB zawsze jest kolorowy?",
            "Nie. Jeżeli kanały R, G i B są równe w każdym pikselu, obraz przedstawia skalę szarości.",
            "Is an RGB image always colorful?",
            "No. If R, G and B match at every pixel, the image is grayscale.",
        ),
        (
            "Czy to prawdziwy model AI?",
            "Nie. To jawna reguła oparta na pikselach i wymiarach, zgodnie z uproszczonym zakresem zadania.",
            "Is this a trained AI model?",
            "No. It is an explicit pixel and dimension rule, matching the simplified assignment.",
        ),
    ],
    17: [
        (
            "Skąd drugi krok dostaje liczbę?",
            "chain dodaje wynik pierwszego kroku jako argument sygnatury times_ten.s().",
            "Where does the second step get its number?",
            "chain adds the first step's result as an argument to times_ten.s().",
        ),
        (
            "Co jeśli pierwszy krok zawiedzie?",
            "Kolejne kroki nie wykonają zwykłej ścieżki. Produkcyjny łańcuch wymaga też obsługi błędów, nie tylko odczytu wyniku końcowego.",
            "What if the first step fails?",
            "Later steps do not follow the normal path. A production chain also needs error handling, not just reading its final result.",
        ),
    ],
    18: [
        (
            "Czy sama nazwa priority_queue daje priorytet?",
            "Nie. Korzyść pochodzi z oddzielnego workera, który nie jest zajęty zadaniem z default.",
            "Does the name priority_queue create priority?",
            "No. The benefit comes from a separate worker that is not occupied by a default task.",
        ),
        (
            "Dlaczego mail nie trafia do default?",
            "CELERY_TASK_ROUTES dopasowuje pełną nazwę send_notification i wybiera priority_queue.",
            "Why does email avoid default?",
            "CELERY_TASK_ROUTES matches the full send_notification task name and selects priority_queue.",
        ),
    ],
    19: [
        (
            "Skąd Flower wie o wykonaniu?",
            "Workery wysyłają zdarzenia Celery dzięki -E. Flower zbiera zdarzenia i pyta workery o stan.",
            "How does Flower know about executions?",
            "Workers emit Celery events with -E. Flower collects those events and inspects workers.",
        ),
        (
            "Czy Flower wykonuje funkcję zadania?",
            "Nie. Może zlecić zadanie przez broker, ale wykonanie nadal należy do workera.",
            "Does Flower execute task functions?",
            "No. It can submit a task through the broker, but a worker still performs the execution.",
        ),
    ],
    20: [
        (
            "Co może się stać przy .delay() przed COMMIT?",
            "Worker używa innego połączenia do bazy i może nie zobaczyć nowego rekordu. Wynik zależy od kolejności zdarzeń.",
            "What can happen with .delay() before COMMIT?",
            "The worker uses another database connection and may not see the new row. The outcome depends on event ordering.",
        ),
        (
            "Czy callback wykona się po rollback?",
            "Nie. Django odrzuca callback zarejestrowany w wycofanej transakcji. Przykład rollback nie wysyła zadania.",
            "Will the callback run after rollback?",
            "No. Django discards callbacks from a rolled-back transaction. The rollback example publishes no task.",
        ),
        (
            "Czy on_commit gwarantuje dostarczenie do brokera?",
            "Nie. Commit mógł się udać, a publikacja potem zawieść. Dla mocniejszych gwarancji stosuje się np. transactional outbox.",
            "Does on_commit guarantee broker delivery?",
            "No. Commit can succeed and publication later fail. Stronger guarantees can use a transactional outbox.",
        ),
    ],
}

OPERATIONS = {
    3: (
        "localtime() tworzy czas w strefie projektu. open(..., 'a') otwiera plik do dopisywania; write dodaje datę i znak nowej linii.",
        "localtime() uses the project timezone. open(..., 'a') opens the file for appending; write adds the date and a newline.",
    ),
    4: (
        "Worker wykonuje tę samą funkcję log_timestamp co w zadaniu 3. Różni się producent: zamiast przycisku wiadomości publikuje Beat.",
        "The worker executes the same log_timestamp function as exercise 3. The producer differs: Beat publishes messages instead of the button.",
    ),
    5: (
        "get_user_model() wskazuje model użytkownika Django. objects.count() zwraca liczbę rekordów. print zapisuje liczbę w logu, return oddaje ją przeglądarce.",
        "get_user_model() identifies Django's user model. objects.count() returns the number of rows. print logs the count; return provides it to the browser.",
    ),
    6: (
        "Ponownie używamy count_users. Funkcja nie zna harmonogramu: reguła w settings.py określa, kiedy Beat ma ją zlecić.",
        "We reuse count_users. The function does not know its schedule: a settings.py rule tells Beat when to submit it.",
    ),
    7: (
        "get(pk=user_id) pobiera rekord po kluczu głównym. timezone.now() ustawia datę, a save(update_fields=...) zapisuje tylko last_login.",
        "get(pk=user_id) loads the row by primary key. timezone.now() sets the timestamp; save(update_fields=...) writes only last_login.",
    ),
    8: (
        "sleep zatrzymuje wykonanie tej funkcji na 15 sekund. Dopiero później return zapisuje komunikat zakończenia w backendzie wyników.",
        "sleep pauses this function for fifteen seconds. Only afterwards does return store the completion message in the result backend.",
    ),
    9: (
        "Worker używa funkcji multiply z zadania 2. Komenda jest producentem: losuje pary argumentów i pięćdziesiąt razy publikuje zadanie.",
        "The worker uses multiply from exercise 2. The command is the producer: it generates argument pairs and publishes fifty tasks.",
    ),
    10: (
        "Pobieramy powiadomienie po ID, symulujemy wysyłkę przez sleep(2), ustawiamy sent_at i zapisujemy zmienione pole.",
        "We load the notification by ID, simulate sending with sleep(2), set sent_at and save that field.",
    ),
    11: (
        "range(1, 101) daje liczby 1–100. W każdej iteracji sleep(0.1) symuluje pracę, a update_state publikuje current i total.",
        "range(1, 101) yields 1–100. Each iteration sleeps for 0.1 seconds and update_state publishes current and total.",
    ),
    12: (
        "cutoff wyznacza granicę 90 dni. filter wybiera stare logi, delete usuwa je z bazy i zwraca liczbę usuniętych rekordów.",
        "cutoff defines the ninety-day boundary. filter selects old logs; delete removes them and returns the deletion count.",
    ),
    13: (
        "requests pobiera HTML. BeautifulSoup znajduje title i usuwa otaczające odstępy. objects.create zapisuje tytuł wraz z URL.",
        "requests fetches HTML. BeautifulSoup finds title and strips surrounding whitespace. objects.create saves the title with its URL.",
    ),
    14: (
        "Tworzymy osobny plik z task_id w nazwie. csv.writer zapisuje nagłówek i dane użytkowników; iterator odczytuje rekordy partiami.",
        "We create a separate file named with task_id. csv.writer writes the header and user data; iterator reads rows in batches.",
    ),
    15: (
        "requests.get próbuje połączyć się z adresem .invalid. except przechwytuje błąd sieci; raise self.retry publikuje ponowienie i przerywa obecną próbę.",
        "requests.get attempts the .invalid address. except catches a network error; raise self.retry publishes a retry and ends the current attempt.",
    ),
    16: (
        "Pillow otwiera zapisany plik, konwertuje go do RGB i rozdziela kanały. Równe kanały oznaczają szarość; wynik zawiera też szerokość i wysokość.",
        "Pillow opens the saved image, converts it to RGB and splits its channels. Matching channels indicate grayscale; the result also includes width and height.",
    ),
    17: (
        "random_number losuje liczbę 1–100. times_ten przyjmuje wynik i mnoży go przez 10. save_number zapisuje końcową wartość w osobnym pliku.",
        "random_number generates a value from 1 to 100. times_ten receives it and multiplies by ten. save_number writes the final value into a separate file.",
    ),
    18: (
        "Funkcja mailowa jest wspólna z zadaniem 10. Routing kieruje ją do priority_queue, dlatego wykonuje ją osobny worker.",
        "The email function is shared with exercise 10. Routing sends it to priority_queue, so a separate worker executes it.",
    ),
    19: (
        "Flower publikuje hello_world przez własne API. Worker nadal wykonuje tę samą funkcję z zadania 1, a zdarzenia pojawiają się w monitorze.",
        "Flower publishes hello_world through its API. A worker executes the same function from exercise 1 and events appear in the monitor.",
    ),
    20: (
        "Worker pobiera zatwierdzony rekord, zamienia text na wielkie litery i zapisuje processed_at. Dzięki on_commit rekord istnieje przed zleceniem.",
        "The worker loads the committed row, uppercases text and saves processed_at. on_commit ensures the record exists before submission.",
    ),
}


def get_curriculum(number):
    (
        assignment,
        concept_pl,
        concept_en,
        pitfall_pl,
        pitfall_en,
        anchor,
        anchor2,
        sample,
    ) = LESSONS[number]
    original = (Path(__file__).resolve().parent.parent / "tasks.md").read_text(
        encoding="utf-8"
    )
    block = re.split(r"## TASK \d+[^\n]*\n", original)[number]
    plain = re.sub(
        r"</?(?:p|strong)[^>]*>|```\w*|`|> \[!tip\]|^> ?",
        "",
        block,
        flags=re.MULTILINE,
    ).strip()
    intros = [
        {
            "pl": [
                "Treść zadania",
                plain,
                "Przykład w aplikacji wykonuje prawdziwe zadanie Celery.",
                "Najpierw poznaj mechanizm, potem uruchom przykład i przeanalizuj kod.",
            ],
            "en": [
                "The assignment",
                assignment,
                "The app example executes a real Celery task.",
                "Understand the mechanism, run an example, then inspect the code.",
            ],
        },
        {
            "pl": [
                concept_pl,
                pitfall_pl,
                "Django zleca pracę. Worker wykonuje kod w osobnym procesie.",
                "Identyfikator zadania pozwala obserwować wynik bez blokowania widoku.",
            ],
            "en": [
                concept_en,
                pitfall_en,
                "Django submits work. A worker executes the code in a separate process.",
                "The task ID lets you observe its result without blocking the view.",
            ],
        },
        {
            "pl": [
                "Przepływ danych",
                sample,
                "W przykładach zobaczysz wynik oraz historię swoich wywołań.",
                "Kod na slajdach pochodzi z rzeczywistych plików tej aplikacji.",
            ],
            "en": [
                "Data flow",
                sample,
                "Examples show results and the history of your submissions.",
                "Slide code comes from the actual application files.",
            ],
        },
        {
            "pl": [
                "Co sprawdzić?",
                pitfall_pl,
                "Porównaj odpowiedź po zleceniu z wynikiem po zakończeniu.",
                "Harmonogramy dzienne i godzinowe działają o wskazanej porze; przycisk pozwala sprawdzić tę samą funkcję od razu.",
            ],
            "en": [
                "What should you check?",
                pitfall_en,
                "Compare the submission response with the final result.",
                "Daily and hourly schedules run at their configured times; the button tests the same function immediately.",
            ],
        },
    ]
    if number == 20:
        from .transaction_explanation import PAGES

        intros = [intros[0], *PAGES]
    from .solution_steps import get_solution_steps

    steps = get_solution_steps(number, anchor, *OPERATIONS[number])
    questions = [
        {"pl": [pl_q, pl_a], "en": [en_q, en_a]}
        for pl_q, pl_a, en_q, en_a in TASK_QUESTIONS[number]
    ]
    return {
        "intros": intros,
        "steps": steps,
        "questions": questions,
        "sample": sample,
        "pl": pitfall_pl,
        "en": pitfall_en,
    }
