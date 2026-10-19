# Uruchamianie całego kursu

Wspólne środowisko znajduje się w `.venv` w głównym katalogu kursu.
Na tym komputerze używa Python 3.12.14. Lokalna baza interpretera jest w
`.python-runtime`; oba katalogi są pomijane przez Git. Nie kopiuj `.venv`
między komputerami. Na innym komputerze zainstaluj Python 3.12 i odtwórz środowisko.

## Przygotowanie

Z głównego katalogu kursu:

```powershell
python setup_course.py
.\.venv\Scripts\Activate.ps1
python run_lesson.py lessons/lesson01/task1_hello.py
```

Na tym komputerze można od razu używać:

```powershell
.\.venv\Scripts\python.exe run_lesson.py lessons/lesson01/task1_hello.py
```

`run_lesson.py` wybiera wspólny interpreter i ustawia katalog roboczy na katalog
wybranego skryptu. Zapobiega to problemom ze względnymi ścieżkami do plików.
W edytorze wybierz `.venv/Scripts/python.exe` z głównego katalogu kursu.

## Aplikacje

```powershell
.\.venv\Scripts\python.exe lessons/lesson20/myproject/runserver.py
.\.venv\Scripts\python.exe lessons/lesson20/myproject/runserver.py --check
.\.venv\Scripts\python.exe lessons/lesson28/api_lab/run_app.py
.\.venv\Scripts\python.exe lessons/lesson29/run_app.py --local-queue
```

Skrypty `runserver.py` sprawdzają projekt, wykonują istniejące migracje, a potem
uruchamiają serwer. `--check` sprawdza samą konfigurację, `--no-migrate` pomija
migracje, `--port 8030` pozwala zmienić port. Nowe migracje modeli twórz jawnie
przez `manage.py makemigrations`. Skrypty nie generują ich automatycznie.

Skrypty instalacyjne lekcji wywołują wspólny `setup_course.py`.
Pliki `requirements.txt` lekcji odsyłają do wspólnej listy. Skrypty bootstrap
nie nadpisują już zależności pakietami z przypadkowego aktywnego środowiska.

## Zależności i inne komputery

`requirements.txt` zawiera biblioteki używane w kodzie i materiałach lekcji 1–38.
`requirements-lock.txt` przechowuje wersje sprawdzone na tym Windows.
Instalator używa wspólnej listy oraz tego pliku jako ograniczeń wersji:

```powershell
python -m pip install -r requirements.txt -c requirements-lock.txt
python -m pip check
```

Zależności zależne od systemu są oznaczone warunkami: `pywin32` jest potrzebne
kolejce plikowej Celery na Windows; `gunicorn` jest przeznaczony dla innych systemów.
Pliki środowiska, lokalne bazy, cache i hasła pozostają poza Git.

## Usługi i konfiguracja

Samo pobranie repozytorium nie instaluje Pythona, bibliotek, serwerów ani danych.

- Lekcja 18 domyślnie korzysta z PostgreSQL. Ustaw `DATABASE_URL` w `.env` projektu.
- Projekty PostgreSQL z lekcji 19 i 28 wymagają `.env` z `DJANGO_SECRET_KEY`,
  `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
- Projekt `lesson27/l27_pro_3` wymaga Redis. Jego adres musi wskazywać działającą usługę.
- Lekcja 29 działa bez Dockera z `--local-queue`; tryb Redis wymaga Dockera lub
  odpowiedniego skonfigurowania brokera.
- AWS, OpenAI i przykłady HTTP wymagają odpowiednio kont, kluczy lub dostępu do sieci.

Gdy drugi komputer z PostgreSQL lub Redis jest wyłączony, ćwiczenia używające
jego usług nie połączą się z nimi. Instalacja pakietów nie zastępuje tych serwerów.

## Kontrola kodu

`audit_course.py` sprawdza składnię i niezdefiniowane nazwy, konfigurację Django,
wybrane programy z przykładowym wejściem, aplikacje Flask, programy SQL oraz testy
Django. Testy aplikacji korzystają z tymczasowych kopii i testowych baz SQLite.
`audit_startups.py` sprawdza uruchamianie serwerów i odpowiedzi lokalnego HTTP.
Wyniki zapisują się w `audit-results.json` i `startup-results.json`.

Kontrole SQLite nie potwierdzają połączeń z docelowymi serwerami PostgreSQL/Redis.
Sprawdzono składnię 531 plików, konfigurację 14 projektów Django, 33 istniejące
testy Django, pięć aplikacji Flask i cztery aplikacje konsolowe SQL. Potwierdzono
start 14 serwerów Django oraz launcherów API Lab i Celery Lab. Worker Celery
wykonał zadanie `6 × 7` i zwrócił `42`.

Automatyczne próby nie obejmują każdego możliwego wejścia użytkownika, fragmentów
kodu w materiałach Markdown, usług AWS/OpenAI ani całej konfiguracji Docker.

## Przyczyna problemów tego komputera

Windows blokował moduł `_ctypes` starego lokalnego Pythona 3.12.13 komunikatem
„Zasady kontroli aplikacji zablokowały ten plik”. Blokada przerywała importy Django,
Flask i części narzędzi. Użyto działającego lokalnego runtime 3.12.14 dostarczonego
z aplikacją; nie zmieniano zasad bezpieczeństwa Windows.

Dodatkowo lekcje miały sprzeczne wersje bibliotek, kilka osobnych środowisk,
brakujące zależności Windows i skrypty pomijające migracje. W lekcji 29
`Path.as_uri()` kodowało spacje jako `%20`, których backend plikowy Celery nie
dekodował. Poprawiono też nazwę opcji `processed_folder`. Dlatego ten sam kod
mógł działać w katalogu `PythonPro-Course`, lecz nie w `Python Pro Course`. Środowisko na drugim
koncie mogło już zawierać biblioteki, `.env`, bazy i działające usługi, których Git
nie przenosi. Jego działania nie można potwierdzić bez sprawdzenia na tym koncie.

## Scalenie zmian

Nie potrzeba stałej gałęzi osobnej dla komputera. Poprawki przenośności powinny
trafić do wspólnego kodu. Można je najpierw zrecenzować na tymczasowej gałęzi,
np. `shared-course-env`.

Potencjalne konflikty dotyczą plików zależności, launcherów i instrukcji, jeśli
równolegle zmieniano je na drugim koncie. `.venv`, `.python-runtime`, `.env` i lokalne
bazy nie powinny być scalane. Po scaleniu na każdym komputerze uruchom
`setup_course.py`, wybierz wspólny interpreter i wykonaj migracje wybranego projektu.
