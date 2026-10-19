# Celery Lab — wszystkie 20 zadań lekcji 29

Uruchom z katalogu kursu:

```powershell
.venv\Scripts\python.exe lessons\lesson29\run_app.py
```

Launcher uruchamia Docker Desktop w razie potrzeby, Redis, migracje i dane demonstracyjne,
dwa workery Celery, Beat, Flower oraz Django. Otwiera http://127.0.0.1:8029/.
Flower działa na http://127.0.0.1:5559/. Ctrl+C zatrzymuje procesy aplikacji; Redis pozostaje uruchomiony.
Ponowne uruchomienie `run_app.py` zatrzymuje poprzednią aplikację i jej usługi,
a następnie uruchamia świeżą wersję. Rozpoznaje wyłącznie lekcję 29 z tego katalogu;
nie zatrzymuje obcych aplikacji zajmujących port. Adresy CSS i JavaScript zawierają
wersję pliku, dlatego po odświeżeniu strony przeglądarka pobiera aktualne zmiany.
Logi procesów są w `.runtime/{worker,priority,beat,flower,django}.log`.
Opcje: `--no-browser`, `--port 8030`, `--local-queue` (broker plikowy zamiast Redisa).

Wymagane biblioteki:

```powershell
.venv\Scripts\python.exe -m pip install -r lessons\lesson29\requirements.txt
```

## Prezentacja

20 aktywnych kafelków, cztery w wierszu na dużym ekranie. Każde zadanie otwiera wstęp.
Wspólne menu: Wstęp, Przykłady zastosowania, Rozwiązanie krok po kroku, Cały kod, Pytania.
PL/ENG i Slajdy/Tryb ciągły zachowują wybór. Pytania mają ukryte odpowiedzi.
Kod jest odczytywany z aktualnych plików i kolorowany przez Pygments paletą inspirowaną VS Code Dark.
Pasek po lewej otwiera przewijaną listę zadań; końcowe przyciski prowadzą do następnego zadania i katalogu.

## Wykonane zadania

| Zadania | Funkcje |
|---|---|
| 1–4 | hello_world, mnożenie, log.txt, Beat co 10 sekund |
| 5–7 | zliczanie użytkowników, crontab 23:00 Europe/Warsaw, aktualizacja last_login przez ID |
| 8–11 | symulacja filmu 15 s, komenda enqueue_tasks (50 zleceń), EmailNotification, postęp 1–100 |
| 12–15 | retencja logów 90 dni codziennie 00:15, scraping example.com co godzinę, CSV, 3 ponowienia co 60 s |
| 16–20 | Pillow i UploadedImage, chain, dwie kolejki, Flower, transaction.on_commit i rollback |

`default` obsługuje worker domyślny, `priority_queue` osobny worker dla `send_notification`.
Oba używają `solo`: każde wykonuje jedno zadanie naraz. Długie zadanie może opóźniać kolejne
wiadomości i odpowiedzi na inspekcję. Flower zbiera prawdziwe zdarzenia (`-E`).
Zadanie 19 udostępnia panel Workers/Dashboard i Tasks; przycisk zleca zadanie przez rzeczywiste API Flower.
API jest dostępne bez logowania wyłącznie na lokalnym adresie 127.0.0.1, do tego ćwiczenia.

Baza SQLite: `.runtime/lesson.sqlite3`. Dane demonstracyjne: anna, jan, alex i przykładowe logi.
`seed_lesson` uzupełnia brakujące przykładowe rekordy przy uruchomieniu.
Zadanie 12 rzeczywiście usuwa stare logi demonstracyjne. Zadanie 10 symuluje wysyłkę maila.
Zadanie 15 celowo kończy się FAILURE po pierwszej próbie i trzech ponowieniach;
oczekiwanie wynosi około trzech minut. Zadanie 16 stosuje prostą regułę, bez modelu AI.
CSV i pliki łańcucha trafiają do `media/`; link pojawia się po SUCCESS.
`on_commit` zapobiega publikacji przed zatwierdzeniem i pomija rollback, ale nie gwarantuje
atomowego zapisu do bazy i brokera. To lokalna aplikacja edukacyjna.

## Komenda zadania 9

W osobnym terminalu, w katalogu lesson29, użyj tego samego brokera co launcher:

```powershell
$env:LESSON29_BROKER_URL = "redis://127.0.0.1:6389/0"
..\..\.venv\Scripts\python.exe manage.py enqueue_tasks
```

Komenda wypisuje listę 50 identyfikatorów i argumentów jako JSON.

## Sprawdzenie

```powershell
.venv\Scripts\python.exe lessons\lesson29\manage.py check
.venv\Scripts\python.exe lessons\lesson29\manage.py test learning
```

Testy obejmują CSRF, walidację, granicę retencji, commit/rollback, parametry retry
oraz poprawność odwołań slajdów do kodu. Weryfikacja integracyjna wykonuje zadania
z prawdziwymi workerami, pobiera CSV i obserwuje PROGRESS oraz RETRY.

Dokumentacja: [Celery](https://docs.celeryq.dev/en/stable/),
[Django on_commit](https://docs.djangoproject.com/en/5.2/topics/db/transactions/#performing-actions-after-commit),
[Flower API](https://flower.readthedocs.io/en/latest/api.html).

## Lesson29 Task Map

Mapa znaczników odpowiada układowi README lekcji 25–27. Każdy wpis wskazuje rzeczywisty komentarz w kodzie. Wspólna funkcja może mieć kilka osobnych znaczników.

### Tagged Locations

#### [academy/settings.py](academy/settings.py)

- `# TASK 18` — wiersz 65: `CELERY_TASK_DEFAULT_QUEUE = "default"`
- `# TASK 18` — wiersz 67: `CELERY_TASK_ROUTES = {`
- `# TASK 04` — wiersz 76: `"timestamp-every-ten-seconds": {`
- `# TASK 06` — wiersz 81: `"users-at-23": {`
- `# TASK 12` — wiersz 86: `"daily-log-cleanup": {`
- `# TASK 13` — wiersz 91: `"hourly-page-title": {`

#### [academy/urls.py](academy/urls.py)

- `# TASK 01` — wiersz 8: `path("tasks/1/run/", views.run_hello, name="run_hello"),`
- `# TASK 02` — wiersz 10: `path("tasks/2/run/", views.run_multiply, name="run_multiply"),`
- `# TASK 11` — wiersz 14: `path("task-status/<uuid:task_id>/", views.task_status),`
- `# TASK 14` — wiersz 16: `path("tasks/status/<uuid:task_id>/", views.task_status, name="task_status"),`
- `# TASK 14` — wiersz 22: `urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
- `# TASK 16` — wiersz 23: `urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
- `# TASK 17` — wiersz 24: `urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`

#### [learning/management/commands/enqueue_tasks.py](learning/management/commands/enqueue_tasks.py)

- `# TASK 09` — wiersz 7: `class Command(BaseCommand):`

#### [learning/models.py](learning/models.py)

- `# TASK 10` — wiersz 5: `class EmailNotification(models.Model):`
- `# TASK 18` — wiersz 6: `class EmailNotification(models.Model):`
- `# TASK 12` — wiersz 14: `class LogEntry(models.Model):`
- `# TASK 13` — wiersz 20: `class ScrapedPage(models.Model):`
- `# TASK 16` — wiersz 27: `class UploadedImage(models.Model):`
- `# TASK 20` — wiersz 33: `class ProcessingRecord(models.Model):`

#### [learning/static/learning/course-data.js](learning/static/learning/course-data.js)

- `// TASK 01` — wiersz 1: `const translations = {`

#### [learning/static/learning/task-two.js](learning/static/learning/task-two.js)

- `// TASK 02` — wiersz 1: `window.taskIntroduction = [{`

#### [learning/tasks.py](learning/tasks.py)

- `# TASK 01` — wiersz 4: `def hello_world():`
- `# TASK 02` — wiersz 13: `def multiply(a, b):`
- `# TASK 09` — wiersz 14: `def multiply(a, b):`
- `# TASK 03` — wiersz 42: `def log_timestamp():`
- `# TASK 04` — wiersz 43: `def log_timestamp():`
- `# TASK 05` — wiersz 52: `def count_users():`
- `# TASK 06` — wiersz 53: `def count_users():`
- `# TASK 07` — wiersz 61: `def update_user_last_login(user_id):`
- `# TASK 08` — wiersz 70: `def process_video():`
- `# TASK 10` — wiersz 77: `def send_notification(notification_id):`
- `# TASK 18` — wiersz 78: `def send_notification(notification_id):`
- `# TASK 11` — wiersz 93: `def track_progress(self):`
- `# TASK 12` — wiersz 102: `def clean_logs():`
- `# TASK 13` — wiersz 110: `def scrape_title():`
- `# TASK 14` — wiersz 122: `def generate_csv(self):`
- `# TASK 15` — wiersz 147: `def retry_connection(self):`
- `# TASK 16` — wiersz 158: `def classify_image(image_id):`
- `# TASK 17` — wiersz 179: `def random_number():`
- `# TASK 17` — wiersz 185: `def times_ten(number):`
- `# TASK 17` — wiersz 191: `def save_number(self, number):`
- `# TASK 20` — wiersz 200: `def process_record(record_id):`

#### [learning/views.py](learning/views.py)

- `# TASK 01` — wiersz 89: `def run_hello(request):`
- `# TASK 02` — wiersz 100: `def run_multiply(request):`
- `# TASK 11` — wiersz 122: `def task_status(request, task_id):`
- `# TASK 14` — wiersz 123: `def task_status(request, task_id):`
- `# TASK 03` — wiersz 163: `if task_number in (3, 4):`
- `# TASK 04` — wiersz 164: `if task_number in (3, 4):`
- `# TASK 05` — wiersz 167: `elif task_number in (5, 6):`
- `# TASK 06` — wiersz 168: `elif task_number in (5, 6):`
- `# TASK 07` — wiersz 171: `elif task_number == 7:`
- `# TASK 08` — wiersz 177: `elif task_number == 8:`
- `# TASK 09` — wiersz 180: `elif task_number == 9:`
- `# TASK 10` — wiersz 193: `elif task_number in (10, 18):`
- `# TASK 18` — wiersz 194: `elif task_number in (10, 18):`
- `# TASK 11` — wiersz 206: `elif task_number == 11:`
- `# TASK 12` — wiersz 209: `elif task_number == 12:`
- `# TASK 13` — wiersz 212: `elif task_number == 13:`
- `# TASK 14` — wiersz 215: `elif task_number == 14:`
- `# TASK 15` — wiersz 218: `elif task_number == 15:`
- `# TASK 16` — wiersz 221: `elif task_number == 16:`
- `# TASK 17` — wiersz 231: `elif task_number == 17:`
- `# TASK 19` — wiersz 238: `elif task_number == 19:`
- `# TASK 20` — wiersz 266: `def create_transaction_record(request):`
- `# TASK 20` — wiersz 274: `transaction.on_commit(`

#### [requirements.txt](requirements.txt)

- `# TASK 13` — wiersz 5: `requests>=2.32,<3`
- `# TASK 15` — wiersz 6: `requests>=2.32,<3`
- `# TASK 13` — wiersz 8: `beautifulsoup4>=4.12,<5`
- `# TASK 16` — wiersz 10: `Pillow>=11,<13`
- `# TASK 19` — wiersz 12: `flower>=2.0,<3`

#### [run_app.py](run_app.py)

- `# TASK 18` — wiersz 231: `worker = logged_process(`
- `# TASK 18` — wiersz 276: `priority = logged_process(`
- `# TASK 04` — wiersz 298: `beat = logged_process(`
- `# TASK 06` — wiersz 299: `beat = logged_process(`
- `# TASK 12` — wiersz 300: `beat = logged_process(`
- `# TASK 13` — wiersz 301: `beat = logged_process(`
- `# TASK 19` — wiersz 319: `flower = logged_process(`

### Pliki wspólne i generowane

`academy/celery.py` zawiera wspólne połączenie Django z Celery. `learning/curriculum.py`, szablony i style tworzą wspólną prezentację dydaktyczną. `manage.py`, inicjalizatory pakietów i migracje są szkieletem projektu. Baza, logi i pliki w `media/` są danymi uruchomieniowymi, bez znaczników.

`tasks.md` zawiera treść zadań `TASK 01`–`TASK 20`. Aby wyszukać rozwiązanie w edytorze, szukaj np. `# TASK 11` w katalogu lekcji.
